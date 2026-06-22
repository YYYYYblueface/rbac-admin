from sqlalchemy import Column, DateTime, Enum, Integer, String, func
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.role import StatusEnum


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="权限ID")
    name = Column(String(64), unique=True, nullable=False, comment="权限名称")
    code = Column(String(128), unique=True, nullable=False, index=True, comment="权限编码")
    description = Column(String(256), nullable=True, comment="权限描述")
    status = Column(
        Enum(StatusEnum), default=StatusEnum.ACTIVE, nullable=False, comment="状态"
    )
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )

    roles = relationship("Role", secondary="role_permissions", back_populates="permissions", lazy="selectin")