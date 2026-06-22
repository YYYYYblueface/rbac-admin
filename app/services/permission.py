from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.permission import Permission
from app.schemas.permission import PermissionCreate, PermissionUpdate


class PermissionService:
    @staticmethod
    async def get_list(
        db: AsyncSession,
        page: int = 1,
        page_size: int = 10,
        name: Optional[str] = None,
    ) -> dict:
        query = select(Permission)
        count_query = select(func.count(Permission.id))

        if name:
            query = query.where(Permission.name.contains(name))
            count_query = count_query.where(Permission.name.contains(name))

        total_result = await db.execute(count_query)
        total = total_result.scalar()

        query = query.offset((page - 1) * page_size).limit(page_size).order_by(Permission.id.desc())
        result = await db.execute(query)
        permissions = result.scalars().all()

        return {"total": total, "items": permissions}

    @staticmethod
    async def get_by_id(db: AsyncSession, perm_id: int) -> Optional[Permission]:
        result = await db.execute(select(Permission).where(Permission.id == perm_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, data: PermissionCreate) -> Permission:
        result = await db.execute(select(Permission).where(Permission.code == data.code))
        if result.scalar_one_or_none():
            raise ValueError(f"权限编码 {data.code} 已存在")

        perm = Permission(
            name=data.name,
            code=data.code,
            description=data.description,
            status=data.status,
        )
        db.add(perm)
        await db.flush()
        await db.refresh(perm)
        return perm

    @staticmethod
    async def update(db: AsyncSession, perm_id: int, data: PermissionUpdate) -> Permission:
        perm = await PermissionService.get_by_id(db, perm_id)
        if perm is None:
            raise ValueError("权限不存在")

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(perm, key, value)

        await db.flush()
        await db.refresh(perm)
        return perm

    @staticmethod
    async def delete(db: AsyncSession, perm_id: int) -> None:
        perm = await PermissionService.get_by_id(db, perm_id)
        if perm is None:
            raise ValueError("权限不存在")
        await db.delete(perm)
        await db.flush()