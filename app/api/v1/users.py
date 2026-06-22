from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user, require_permission
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.user import UserService
from app.utils.response import fail, success

router = APIRouter(prefix="/users", tags=["用户管理"])


@router.get("", response_model=dict)
async def get_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    username: str = Query(None),
    status: str = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission(["user:list"])),
):
    result = await UserService.get_list(db, page, page_size, username, status)
    return success(data=result)


@router.get("/{user_id}", response_model=dict)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission(["user:list"])),
):
    user = await UserService.get_by_id(db, user_id)
    if user is None:
        return fail(code=404, message="用户不存在")
    return success(data=user)


@router.post("", response_model=dict)
async def create_user(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission(["user:create"])),
):
    try:
        user = await UserService.create(db, data)
        return success(data=user, message="创建成功")
    except ValueError as e:
        return fail(code=400, message=str(e))


@router.put("/{user_id}", response_model=dict)
async def update_user(
    user_id: int,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission(["user:update"])),
):
    try:
        user = await UserService.update(db, user_id, data)
        return success(data=user, message="更新成功")
    except ValueError as e:
        return fail(code=400, message=str(e))


@router.delete("/{user_id}", response_model=dict)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission(["user:delete"])),
):
    try:
        await UserService.delete(db, user_id)
        return success(message="删除成功")
    except ValueError as e:
        return fail(code=400, message=str(e))