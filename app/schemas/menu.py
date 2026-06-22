from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class MenuBase(BaseModel):
    parent_id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=64)
    path: Optional[str] = Field(None, max_length=256)
    component: Optional[str] = Field(None, max_length=256)
    icon: Optional[str] = Field(None, max_length=64)
    sort: int = 0
    status: str = "active"


class MenuCreate(MenuBase):
    pass


class MenuUpdate(BaseModel):
    parent_id: Optional[int] = None
    name: Optional[str] = Field(None, min_length=1, max_length=64)
    path: Optional[str] = Field(None, max_length=256)
    component: Optional[str] = Field(None, max_length=256)
    icon: Optional[str] = Field(None, max_length=64)
    sort: Optional[int] = None
    status: Optional[str] = None


class MenuResponse(MenuBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    children: List["MenuResponse"] = []

    model_config = {"from_attributes": True}


class MenuTreeResponse(BaseModel):
    items: List[MenuResponse]