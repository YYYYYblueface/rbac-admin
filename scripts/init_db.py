"""
数据库初始化脚本
用途：首次部署时，创建默认超级管理员、角色和权限
运行方式：python scripts/init_db.py
"""
import asyncio
import sys

sys.path.insert(0, ".")

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import engine, async_session_factory, Base
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.models.menu import Menu
from app.utils.security import hash_password


# 默认权限列表
DEFAULT_PERMISSIONS = [
    {"name": "用户列表", "code": "user:list"},
    {"name": "创建用户", "code": "user:create"},
    {"name": "更新用户", "code": "user:update"},
    {"name": "删除用户", "code": "user:delete"},
    {"name": "角色列表", "code": "role:list"},
    {"name": "创建角色", "code": "role:create"},
    {"name": "更新角色", "code": "role:update"},
    {"name": "删除角色", "code": "role:delete"},
    {"name": "权限列表", "code": "perm:list"},
    {"name": "创建权限", "code": "perm:create"},
    {"name": "更新权限", "code": "perm:update"},
    {"name": "删除权限", "code": "perm:delete"},
    {"name": "菜单列表", "code": "menu:list"},
    {"name": "创建菜单", "code": "menu:create"},
    {"name": "更新菜单", "code": "menu:update"},
    {"name": "删除菜单", "code": "menu:delete"},
]

# 默认菜单列表
DEFAULT_MENUS = [
    {"name": "系统管理", "path": "/system", "icon": "Setting", "sort": 1, "children": [
        {"name": "用户管理", "path": "/system/users", "icon": "User", "sort": 1},
        {"name": "角色管理", "path": "/system/roles", "icon": "UserFilled", "sort": 2},
        {"name": "权限管理", "path": "/system/permissions", "icon": "Key", "sort": 3},
        {"name": "菜单管理", "path": "/system/menus", "icon": "Menu", "sort": 4},
    ]},
]


async def init_db():
    print("正在创建数据库表...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("数据库表创建完成")

    async with async_session_factory() as db:
        # 创建权限
        permissions = []
        for perm_data in DEFAULT_PERMISSIONS:
            result = await db.execute(select(Permission).where(Permission.code == perm_data["code"]))
            existing = result.scalar_one_or_none()
            if existing is None:
                perm = Permission(**perm_data, status="active")
                db.add(perm)
                await db.flush()
                permissions.append(perm)
                print(f"  创建权限: {perm.name}")
            else:
                permissions.append(existing)

        # 创建菜单
        menus = []
        for menu_data in DEFAULT_MENUS:
            children = menu_data.pop("children", [])
            menu = Menu(**menu_data, status="active")
            db.add(menu)
            await db.flush()
            menus.append(menu)
            print(f"  创建菜单: {menu.name}")

            for child_data in children:
                child = Menu(**child_data, parent_id=menu.id, status="active")
                db.add(child)
                await db.flush()
                menus.append(child)
                print(f"    创建子菜单: {child.name}")

        # 创建超级管理员角色
        result = await db.execute(select(Role).where(Role.code == "admin"))
        admin_role = result.scalar_one_or_none()
        if admin_role is None:
            admin_role = Role(
                name="超级管理员",
                code="admin",
                description="系统超级管理员",
                status="active",
            )
            admin_role.permissions = permissions
            admin_role.menus = menus
            db.add(admin_role)
            await db.flush()
            print(f"  创建角色: {admin_role.name}")
        else:
            admin_role.permissions = permissions
            admin_role.menus = menus

        # 创建超级管理员用户
        result = await db.execute(select(User).where(User.username == "admin"))
        admin_user = result.scalar_one_or_none()
        if admin_user is None:
            admin_user = User(
                username="admin",
                password=hash_password("admin123"),
                email="admin@example.com",
                is_superuser=True,
                status="active",
            )
            admin_user.roles = [admin_role]
            db.add(admin_user)
            print(f"  创建用户: admin (密码: admin123)")

        await db.commit()
        print("\n初始化完成！")
        print("默认管理员账号: admin / admin123")
        print("请登录后修改默认密码！")


if __name__ == "__main__":
    asyncio.run(init_db())