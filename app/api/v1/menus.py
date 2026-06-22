from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user, require_permission
from app.models.user import User
from app.schemas.menu import MenuCreate, MenuUpdate
from app.services.menu import MenuService
from app.utils.response import fail, serialize, success

router = APIRouter(prefix="/menus", tags=["菜单管理"])


@router.get("/tree", response_model=dict)
async def get_menu_tree(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取菜单树（所有登录用户可访问）"""
    menus = await MenuService.get_tree(db)
    return success(data=serialize(menus))


@router.get("/{menu_id}", response_model=dict)
async def get_menu(
    menu_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission(["menu:list"])),
):
    menu = await MenuService.get_by_id(db, menu_id)
    if menu is None:
        return fail(code=404, message="菜单不存在")
    return success(data=serialize(menu))


@router.post("", response_model=dict)
async def create_menu(
    data: MenuCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission(["menu:create"])),
):
    try:
        menu = await MenuService.create(db, data)
        return success(data=serialize(menu), message="创建成功")
    except ValueError as e:
        return fail(code=400, message=str(e))


@router.put("/{menu_id}", response_model=dict)
async def update_menu(
    menu_id: int,
    data: MenuUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission(["menu:update"])),
):
    try:
        menu = await MenuService.update(db, menu_id, data)
        return success(data=serialize(menu), message="更新成功")
    except ValueError as e:
        return fail(code=400, message=str(e))


@router.delete("/{menu_id}", response_model=dict)
async def delete_menu(
    menu_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission(["menu:delete"])),
):
    try:
        await MenuService.delete(db, menu_id)
        return success(message="删除成功")
    except ValueError as e:
        return fail(code=400, message=str(e))