from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class PermissionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=64)
    code: str = Field(..., min_length=1, max_length=128)
    description: Optional[str] = Field(None, max_length=256)
    status: str = "active"


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=64)
    code: Optional[str] = Field(None, min_length=1, max_length=128)
    description: Optional[str] = Field(None, max_length=256)
    status: Optional[str] = None


class PermissionResponse(PermissionBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class PermissionListResponse(BaseModel):
    total: int
    items: List[PermissionResponse]