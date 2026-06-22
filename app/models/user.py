import enum
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.database import Base


class UserStatus(str, enum.Enum):
    ACTIVE = "active"
    DISABLED = "disabled"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="用户ID")
    username = Column(String(64), unique=True, nullable=False, index=True, comment="用户名")
    password = Column(String(256), nullable=False, comment="密码")
    email = Column(String(128), unique=True, nullable=True, comment="邮箱")
    phone = Column(String(20), nullable=True, comment="手机号")
    avatar = Column(String(512), nullable=True, comment="头像URL")
    status = Column(
        Enum(UserStatus), default=UserStatus.ACTIVE, nullable=False, comment="状态"
    )
    is_superuser = Column(Boolean, default=False, comment="是否超级管理员")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )

    roles = relationship("Role", secondary="user_roles", back_populates="users", lazy="selectin")