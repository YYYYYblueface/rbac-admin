from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user, require_permission
from app.models.user import User
from app.schemas.permission import PermissionCreate, PermissionUpdate
from app.services.permission import PermissionService
from app.utils.response import fail, serialize, success

router = APIRouter(prefix="/permissions", tags=["权限管理"])


@router.get("", response_model=dict)
async def get_permissions(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    name: str = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission(["perm:list"])),
):
    result = await PermissionService.get_list(db, page, page_size, name)
    return success(data=serialize(result))


@router.get("/{perm_id}", response_model=dict)
async def get_permission(
    perm_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission(["perm:list"])),
):
    perm = await PermissionService.get_by_id(db, perm_id)
    if perm is None:
        return fail(code=404, message="权限不存在")
    return success(data=serialize(perm))


@router.post("", response_model=dict)
async def create_permission(
    data: PermissionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission(["perm:create"])),
):
    try:
        perm = await PermissionService.create(db, data)
        return success(data=serialize(perm), message="创建成功")
    except ValueError as e:
        return fail(code=400, message=str(e))


@router.put("/{perm_id}", response_model=dict)
async def update_permission(
    perm_id: int,
    data: PermissionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission(["perm:update"])),
):
    try:
        perm = await PermissionService.update(db, perm_id, data)
        return success(data=serialize(perm), message="更新成功")
    except ValueError as e:
        return fail(code=400, message=str(e))


@router.delete("/{perm_id}", response_model=dict)
async def delete_permission(
    perm_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission(["perm:delete"])),
):
    try:
        await PermissionService.delete(db, perm_id)
        return success(message="删除成功")
    except ValueError as e:
        return fail(code=400, message=str(e))