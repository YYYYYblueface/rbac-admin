from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=64)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    avatar: Optional[str] = Field(None, max_length=512)
    status: str = "active"
    is_superuser: bool = False


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=128)
    role_ids: List[int] = []


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=1, max_length=64)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    avatar: Optional[str] = Field(None, max_length=512)
    status: Optional[str] = None
    is_superuser: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=6, max_length=128)
    role_ids: Optional[List[int]] = None


class UserResponse(UserBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    roles: list = []

    model_config = {"from_attributes": True}


class UserListResponse(BaseModel):
    total: int
    items: List[UserResponse]