from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.role import StatusEnum


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="菜单ID")
    parent_id = Column(
        Integer, ForeignKey("menus.id"), nullable=True, index=True, comment="父菜单ID"
    )
    name = Column(String(64), nullable=False, comment="菜单名称")
    path = Column(String(256), nullable=True, comment="路由路径")
    component = Column(String(256), nullable=True, comment="组件路径")
    icon = Column(String(64), nullable=True, comment="图标")
    sort = Column(Integer, default=0, comment="排序")
    status = Column(
        Enum(StatusEnum), default=StatusEnum.ACTIVE, nullable=False, comment="状态"
    )
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )

    children = relationship("Menu", backref="parent", remote_side=[id], lazy="selectin")
    roles = relationship("Role", secondary="role_menus", back_populates="menus", lazy="selectin")