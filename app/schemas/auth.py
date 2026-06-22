from datetime import datetime

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=64, description="用户名")
    password: str = Field(..., min_length=1, max_length=128, description="密码")
    captcha_key: str = Field(..., description="验证码key")
    captcha_code: str = Field(..., min_length=4, max_length=4, description="验证码")


class TokenResponse(BaseModel):
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field(default="bearer", description="令牌类型")


class CaptchaResponse(BaseModel):
    captcha_key: str = Field(..., description="验证码key")
    captcha_image: str = Field(..., description="验证码图片(base64)")