from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.menu import Menu
from app.schemas.menu import MenuCreate, MenuUpdate


class MenuService:
    @staticmethod
    async def get_tree(db: AsyncSession) -> List[Menu]:
        result = await db.execute(
            select(Menu).order_by(Menu.sort.asc(), Menu.id.asc())
        )
        menus = list(result.scalars().all())
        return MenuService._build_tree(menus)

    @staticmethod
    def _build_tree(menus: List[Menu], parent_id: Optional[int] = None) -> list:
        """构建树形结构，返回新的 dict 列表"""
        tree = []
        for menu in menus:
            if menu.parent_id == parent_id:
                item = {
                    "id": menu.id,
                    "parent_id": menu.parent_id,
                    "name": menu.name,
                    "path": menu.path,
                    "component": menu.component,
                    "icon": menu.icon,
                    "sort": menu.sort,
                    "status": menu.status.value if menu.status else None,
                    "children": MenuService._build_tree(menus, menu.id),
                    "created_at": menu.created_at.isoformat() if menu.created_at else None,
                    "updated_at": menu.updated_at.isoformat() if menu.updated_at else None,
                }
                tree.append(item)
        return tree

    @staticmethod
    async def get_by_id(db: AsyncSession, menu_id: int) -> Optional[Menu]:
        result = await db.execute(select(Menu).where(Menu.id == menu_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, data: MenuCreate) -> Menu:
        menu = Menu(**data.model_dump())
        db.add(menu)
        await db.flush()
        await db.refresh(menu)
        return menu

    @staticmethod
    async def update(db: AsyncSession, menu_id: int, data: MenuUpdate) -> Menu:
        menu = await MenuService.get_by_id(db, menu_id)
        if menu is None:
            raise ValueError("菜单不存在")

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(menu, key, value)

        await db.flush()
        await db.refresh(menu)
        return menu

    @staticmethod
    async def delete(db: AsyncSession, menu_id: int) -> None:
        menu = await MenuService.get_by_id(db, menu_id)
        if menu is None:
            raise ValueError("菜单不存在")
        await db.delete(menu)
        await db.flush()