from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.auth import LoginRequest
from app.utils.captcha import verify_captcha
from app.utils.security import create_access_token, verify_password


class AuthService:
    @staticmethod
    async def login(db: AsyncSession, req: LoginRequest) -> dict:
        """用户登录"""
        # 验证验证码
        if not await verify_captcha(req.captcha_key, req.captcha_code):
            raise ValueError("验证码错误或已过期")

        # 查询用户
        result = await db.execute(
            select(User).where(User.username == req.username)
        )
        user = result.scalar_one_or_none()
        if user is None:
            raise ValueError("用户名或密码错误")

        if user.status.value == "disabled":
            raise ValueError("用户已被禁用")

        if not verify_password(req.password, user.password):
            raise ValueError("用户名或密码错误")

        # 生成 token
        access_token = create_access_token(data={"sub": str(user.id)})
        return {"access_token": access_token, "token_type": "bearer"}