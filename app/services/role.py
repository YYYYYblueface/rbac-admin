from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.permission import Permission
from app.models.role import Role
from app.models.menu import Menu
from app.schemas.role import RoleCreate, RoleUpdate


class RoleService:
    @staticmethod
    async def get_list(
        db: AsyncSession,
        page: int = 1,
        page_size: int = 10,
        name: Optional[str] = None,
        status: Optional[str] = None,
    ) -> dict:
        query = select(Role)
        count_query = select(func.count(Role.id))

        if name:
            query = query.where(Role.name.contains(name))
            count_query = count_query.where(Role.name.contains(name))
        if status:
            query = query.where(Role.status == status)
            count_query = count_query.where(Role.status == status)

        total_result = await db.execute(count_query)
        total = total_result.scalar()

        query = query.offset((page - 1) * page_size).limit(page_size).order_by(Role.id.desc())
        result = await db.execute(query)
        roles = result.scalars().all()

        return {"total": total, "items": roles}

    @staticmethod
    async def get_by_id(db: AsyncSession, role_id: int) -> Optional[Role]:
        result = await db.execute(select(Role).where(Role.id == role_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, data: RoleCreate) -> Role:
        result = await db.execute(select(Role).where(Role.code == data.code))
        if result.scalar_one_or_none():
            raise ValueError(f"角色编码 {data.code} 已存在")

        role = Role(
            name=data.name,
            code=data.code,
            description=data.description,
            status=data.status,
        )

        if data.permission_ids:
            result = await db.execute(select(Permission).where(Permission.id.in_(data.permission_ids)))
            role.permissions = result.scalars().all()

        if data.menu_ids:
            result = await db.execute(select(Menu).where(Menu.id.in_(data.menu_ids)))
            role.menus = result.scalars().all()

        db.add(role)
        await db.flush()
        await db.refresh(role)
        return role

    @staticmethod
    async def update(db: AsyncSession, role_id: int, data: RoleUpdate) -> Role:
        role = await RoleService.get_by_id(db, role_id)
        if role is None:
            raise ValueError("角色不存在")

        update_data = data.model_dump(exclude_unset=True, exclude={"permission_ids", "menu_ids"})

        for key, value in update_data.items():
            setattr(role, key, value)

        if data.permission_ids is not None:
            result = await db.execute(select(Permission).where(Permission.id.in_(data.permission_ids)))
            role.permissions = result.scalars().all()

        if data.menu_ids is not None:
            result = await db.execute(select(Menu).where(Menu.id.in_(data.menu_ids)))
            role.menus = result.scalars().all()

        await db.flush()
        await db.refresh(role)
        return role

    @staticmethod
    async def delete(db: AsyncSession, role_id: int) -> None:
        role = await RoleService.get_by_id(db, role_id)
        if role is None:
            raise ValueError("角色不存在")
        await db.delete(role)
        await db.flush()