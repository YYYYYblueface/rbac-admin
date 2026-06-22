from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class RoleBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=64)
    code: str = Field(..., min_length=1, max_length=64)
    description: Optional[str] = Field(None, max_length=256)
    status: str = "active"


class RoleCreate(RoleBase):
    permission_ids: List[int] = []
    menu_ids: List[int] = []


class RoleUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=64)
    code: Optional[str] = Field(None, min_length=1, max_length=64)
    description: Optional[str] = Field(None, max_length=256)
    status: Optional[str] = None
    permission_ids: Optional[List[int]] = None
    menu_ids: Optional[List[int]] = None


class RoleResponse(RoleBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    permission_ids: List[int] = []
    menu_ids: List[int] = []

    model_config = {"from_attributes": True}