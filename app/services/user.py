from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import Role
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils.security import hash_password


class UserService:
    @staticmethod
    async def get_list(
        db: AsyncSession,
        page: int = 1,
        page_size: int = 10,
        username: Optional[str] = None,
        status: Optional[str] = None,
    ) -> dict:
        query = select(User)
        count_query = select(func.count(User.id))

        if username:
            query = query.where(User.username.contains(username))
            count_query = count_query.where(User.username.contains(username))
        if status:
            query = query.where(User.status == status)
            count_query = count_query.where(User.status == status)

        total_result = await db.execute(count_query)
        total = total_result.scalar()

        query = query.offset((page - 1) * page_size).limit(page_size).order_by(User.id.desc())
        result = await db.execute(query)
        users = result.scalars().all()

        return {"total": total, "items": users}

    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, data: UserCreate) -> User:
        # 检查用户名唯一性
        result = await db.execute(select(User).where(User.username == data.username))
        if result.scalar_one_or_none():
            raise ValueError(f"用户名 {data.username} 已存在")

        user = User(
            username=data.username,
            password=hash_password(data.password),
            email=data.email,
            phone=data.phone,
            avatar=data.avatar,
            status=data.status,
            is_superuser=data.is_superuser,
        )

        if data.role_ids:
            result = await db.execute(select(Role).where(Role.id.in_(data.role_ids)))
            user.roles = result.scalars().all()

        db.add(user)
        await db.flush()
        await db.refresh(user)
        return user

    @staticmethod
    async def update(db: AsyncSession, user_id: int, data: UserUpdate) -> User:
        user = await UserService.get_by_id(db, user_id)
        if user is None:
            raise ValueError("用户不存在")

        update_data = data.model_dump(exclude_unset=True, exclude={"role_ids"})

        if "password" in update_data and update_data["password"]:
            update_data["password"] = hash_password(update_data["password"])

        for key, value in update_data.items():
            setattr(user, key, value)

        if data.role_ids is not None:
            result = await db.execute(select(Role).where(Role.id.in_(data.role_ids)))
            user.roles = result.scalars().all()

        await db.flush()
        await db.refresh(user)
        return user

    @staticmethod
    async def delete(db: AsyncSession, user_id: int) -> None:
        user = await UserService.get_by_id(db, user_id)
        if user is None:
            raise ValueError("用户不存在")
        await db.delete(user)
        await db.flush()