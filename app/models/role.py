import enum

from sqlalchemy import Column, DateTime, Enum, Integer, String, func
from sqlalchemy.orm import relationship

from app.database import Base


class StatusEnum(str, enum.Enum):
    ACTIVE = "active"
    DISABLED = "disabled"


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="角色ID")
    name = Column(String(64), unique=True, nullable=False, comment="角色名称")
    code = Column(String(64), unique=True, nullable=False, index=True, comment="角色编码")
    description = Column(String(256), nullable=True, comment="角色描述")
    status = Column(
        Enum(StatusEnum), default=StatusEnum.ACTIVE, nullable=False, comment="状态"
    )
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )

    users = relationship("User", secondary="user_roles", back_populates="roles", lazy="selectin")
    permissions = relationship("Permission", secondary="role_permissions", back_populates="roles", lazy="selectin")
    menus = relationship("Menu", secondary="role_menus", back_populates="roles", lazy="selectin")