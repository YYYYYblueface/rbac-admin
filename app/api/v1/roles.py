from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user, require_permission
from app.models.user import User
from app.schemas.role import RoleCreate, RoleUpdate
from app.services.role import RoleService
from app.utils.response import fail, success

router = APIRouter(prefix="/roles", tags=["角色管理"])


@router.get("", response_model=dict)
async def get_roles(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    name: str = Query(None),
    status: str = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission(["role:list"])),
):
    result = await RoleService.get_list(db, page, page_size, name, status)
    return success(data=result)


@router.get("/{role_id}", response_model=dict)
async def get_role(
    role_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission(["role:list"])),
):
    role = await RoleService.get_by_id(db, role_id)
    if role is None:
        return fail(code=404, message="角色不存在")
    role_data = {
        "id": role.id,
        "name": role.name,
        "code": role.code,
        "description": role.description,
        "status": role.status.value if role.status else None,
        "permission_ids": [p.id for p in role.permissions],
        "menu_ids": [m.id for m in role.menus],
        "created_at": role.created_at.isoformat() if role.created_at else None,
        "updated_at": role.updated_at.isoformat() if role.updated_at else None,
    }
    return success(data=role_data)


@router.post("", response_model=dict)
async def create_role(
    data: RoleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission(["role:create"])),
):
    try:
        role = await RoleService.create(db, data)
        return success(data=role, message="创建成功")
    except ValueError as e:
        return fail(code=400, message=str(e))


@router.put("/{role_id}", response_model=dict)
async def update_role(
    role_id: int,
    data: RoleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission(["role:update"])),
):
    try:
        role = await RoleService.update(db, role_id, data)
        return success(data=role, message="更新成功")
    except ValueError as e:
        return fail(code=400, message=str(e))


@router.delete("/{role_id}", response_model=dict)
async def delete_role(
    role_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission(["role:delete"])),
):
    try:
        await RoleService.delete(db, role_id)
        return success(message="删除成功")
    except ValueError as e:
        return fail(code=400, message=str(e))