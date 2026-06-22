from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=64, description="用户名")
    password: str = Field(..., min_length=1, max_length=128, description="密码")
    captcha_key: str = Field(..., description="验证码key")
    captcha_code: str = Field(..., min_length=4, max_length=4, description="验证码")