from typing import Any, Optional

from pydantic import BaseModel

from app.models.menu import Menu
from app.models.permission import Permission
from app.models.role import Role
from app.models.user import User


class APIResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: Optional[Any] = None

    model_config = {"from_attributes": True}


def success(data: Any = None, message: str = "success") -> dict:
    return {"code": 200, "message": message, "data": data}


def fail(code: int = 400, message: str = "fail", data: Any = None) -> dict:
    return {"code": code, "message": message, "data": data}


def _serialize(obj: Any) -> Any:
    """递归将 ORM 对象转换为可 JSON 序列化的 dict"""
    if obj is None:
        return None
    if isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, (list, tuple)):
        return [_serialize(item) for item in obj]
    if isinstance(obj, dict):
        return {k: _serialize(v) for k, v in obj.items()}

    # ORM 模型转换
    if isinstance(obj, User):
        return {
            "id": obj.id,
            "username": obj.username,
            "email": obj.email,
            "phone": obj.phone,
            "avatar": obj.avatar,
            "status": obj.status.value if obj.status else None,
            "is_superuser": obj.is_superuser,
            "roles": [_serialize(r) for r in obj.roles] if obj.roles else [],
            "created_at": obj.created_at.isoformat() if obj.created_at else None,
            "updated_at": obj.updated_at.isoformat() if obj.updated_at else None,
        }
    if isinstance(obj, Role):
        return {
            "id": obj.id,
            "name": obj.name,
            "code": obj.code,
            "description": obj.description,
            "status": obj.status.value if obj.status else None,
            "permission_ids": [p.id for p in obj.permissions] if obj.permissions else [],
            "menu_ids": [m.id for m in obj.menus] if obj.menus else [],
            "created_at": obj.created_at.isoformat() if obj.created_at else None,
            "updated_at": obj.updated_at.isoformat() if obj.updated_at else None,
        }
    if isinstance(obj, Permission):
        return {
            "id": obj.id,
            "name": obj.name,
            "code": obj.code,
            "description": obj.description,
            "status": obj.status.value if obj.status else None,
            "created_at": obj.created_at.isoformat() if obj.created_at else None,
            "updated_at": obj.updated_at.isoformat() if obj.updated_at else None,
        }
    if isinstance(obj, Menu):
        return {
            "id": obj.id,
            "parent_id": obj.parent_id,
            "name": obj.name,
            "path": obj.path,
            "component": obj.component,
            "icon": obj.icon,
            "sort": obj.sort,
            "status": obj.status.value if obj.status else None,
            "children": [_serialize(c) for c in obj.children] if obj.children else [],
            "created_at": obj.created_at.isoformat() if obj.created_at else None,
            "updated_at": obj.updated_at.isoformat() if obj.updated_at else None,
        }
    if hasattr(obj, "isoformat"):
        return obj.isoformat()
    return str(obj)


def serialize(data: Any) -> Any:
    """序列化数据为 JSON 安全格式"""
    if isinstance(data, dict):
        if "items" in data and "total" in data:
            return {"total": data["total"], "items": [_serialize(item) for item in data["items"]]}
        return {k: _serialize(v) for k, v in data.items()}
    if isinstance(data, list):
        return [_serialize(item) for item in data]
    return _serialize(data)