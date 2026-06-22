from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1 import auth, menus, permissions, roles, users
from app.config import settings
from app.database import engine, Base
from app.middleware.cors import setup_cors
from app.middleware.exception_handler import setup_exception_handler
from app.middleware.rate_limit import setup_rate_limit
from app.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"{settings.APP_NAME} v{settings.APP_VERSION} 启动中...")
    # 创建所有数据库表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("数据库表初始化完成")
    yield
    await engine.dispose()
    logger.info(f"{settings.APP_NAME} 已关闭")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="通用后台权限管理系统（RBAC）",
    lifespan=lifespan,
)

# 注册中间件
setup_cors(app)
setup_rate_limit(app)
setup_exception_handler(app)

# 注册路由
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(roles.router, prefix="/api/v1")
app.include_router(permissions.router, prefix="/api/v1")
app.include_router(menus.router, prefix="/api/v1")


@app.get("/", tags=["健康检查"])
async def root():
    return {"code": 200, "message": f"{settings.APP_NAME} v{settings.APP_VERSION} 运行正常"}