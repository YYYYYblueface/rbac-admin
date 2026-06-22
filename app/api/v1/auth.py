from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth import CaptchaResponse, LoginRequest, TokenResponse
from app.services.auth import AuthService
from app.utils.captcha import generate_captcha
from app.utils.response import fail, success

router = APIRouter(prefix="/auth", tags=["认证管理"])


@router.post("/login", response_model=dict)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    try:
        result = await AuthService.login(db, req)
        return success(data=result, message="登录成功")
    except ValueError as e:
        return fail(code=400, message=str(e))


@router.get("/captcha", response_model=dict)
async def captcha():
    result = await generate_captcha()
    return success(data=result)


@router.get("/me", response_model=dict)
async def get_me(current_user: User = Depends(get_current_user)):
    """获取当前登录用户信息"""
    user_data = {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "phone": current_user.phone,
        "avatar": current_user.avatar,
        "status": current_user.status.value if current_user.status else None,
        "is_superuser": current_user.is_superuser,
        "roles": [
            {
                "id": r.id,
                "name": r.name,
                "code": r.code,
            }
            for r in current_user.roles
            if r.status.value == "active"
        ],
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
    }
    return success(data=user_data)