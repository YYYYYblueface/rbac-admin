# RBAC Admin - 通用后台权限管理系统

基于 **RBAC（Role-Based Access Control）** 模型的通用后台权限管理系统，提供完整的用户管理、角色管理、权限管理和菜单管理功能。

## 功能特性

- **用户管理**：用户的增删改查，支持分配角色
- **角色管理**：角色的增删改查，支持分配权限和菜单
- **权限管理**：权限的增删改查，细粒度接口权限控制
- **菜单管理**：树形菜单管理，支持无限级嵌套
- **JWT 认证**：基于 JWT 的 Token 认证机制
- **密码加盐加密**：使用 bcrypt 算法对密码进行加盐哈希
- **登录验证码**：图形验证码，存入 Redis 缓存
- **接口限流**：基于 slowapi 的接口访问频率限制
- **日志收集**：基于 loguru 的日志收集，按天滚动
- **跨域支持**：CORS 中间件，支持跨域请求
- **全局异常捕获**：统一异常处理，友好的错误响应
- **统一响应格式**：所有接口返回统一的 JSON 格式

## 技术栈

| 技术 | 说明 |
|------|------|
| Python 3.10 | 编程语言 |
| FastAPI | Web 框架 |
| MySQL 8.0 | 关系型数据库 |
| Redis | 缓存数据库 |
| SQLAlchemy 2.0 | ORM 框架 |
| Pydantic 2.0 | 数据验证 |
| JWT (python-jose) | 认证令牌 |
| passlib + bcrypt | 密码哈希 |
| slowapi | 接口限流 |
| loguru | 日志收集 |
| uvicorn | ASGI 服务器 |

## 开发工具

- **VSCode**：代码编辑器
- **DBeaver**：数据库管理工具
- **Git**：版本管理
- **GitHub**：代码托管

## 项目结构

```
rbac_admin/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 入口
│   ├── config.py               # 应用配置 (pydantic-settings)
│   ├── database.py             # 数据库连接 (SQLAlchemy async)
│   ├── dependencies.py         # 全局依赖注入（JWT认证、权限检查）
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py         # 认证接口（登录/验证码/当前用户）
│   │       ├── users.py        # 用户管理接口
│   │       ├── roles.py        # 角色管理接口
│   │       ├── permissions.py  # 权限管理接口
│   │       └── menus.py        # 菜单管理接口
│   ├── models/
│   │   ├── user.py             # 用户模型
│   │   ├── role.py             # 角色模型
│   │   ├── permission.py       # 权限模型
│   │   ├── menu.py             # 菜单模型
│   │   └── associations.py     # 多对多关联表
│   ├── schemas/
│   │   ├── auth.py             # 认证相关 Schema
│   │   ├── user.py             # 用户 Schema
│   │   ├── role.py             # 角色 Schema
│   │   ├── permission.py       # 权限 Schema
│   │   └── menu.py             # 菜单 Schema
│   ├── services/
│   │   ├── auth.py             # 认证业务逻辑
│   │   ├── user.py             # 用户业务逻辑
│   │   ├── role.py             # 角色业务逻辑
│   │   ├── permission.py       # 权限业务逻辑
│   │   └── menu.py             # 菜单业务逻辑
│   ├── middleware/
│   │   ├── cors.py             # 跨域中间件
│   │   ├── rate_limit.py       # 限流中间件
│   │   └── exception_handler.py # 全局异常处理
│   └── utils/
│       ├── security.py         # JWT + 密码哈希
│       ├── redis_client.py     # Redis 客户端
│       ├── captcha.py          # 图形验证码
│       ├── logger.py           # 日志配置
│       └── response.py         # 统一响应格式
├── scripts/
│   └── init_db.py              # 数据库初始化脚本
├── logs/                       # 日志文件目录
├── requirements.txt            # Python 依赖
├── deploy.sh                   # Linux 部署脚本
├── .env.example                # 环境变量模板
├── .gitignore
└── README.md
```

## 数据库表结构

| 表名 | 说明 |
|------|------|
| users | 用户表 |
| roles | 角色表 |
| permissions | 权限表 |
| menus | 菜单表 |
| user_roles | 用户-角色关联表 |
| role_permissions | 角色-权限关联表 |
| role_menus | 角色-菜单关联表 |

## 快速开始

### 前置条件

- Python 3.10+
- MySQL 8.0+
- Redis 6.0+

### 1. 克隆项目

```bash
git clone https://github.com/your-username/rbac_admin.git
cd rbac_admin
```

### 2. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件，修改数据库和 Redis 配置：

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=rbac_admin

REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_PASSWORD=
```

### 5. 创建数据库

使用 DBeaver 或 MySQL 命令行创建数据库：

```sql
CREATE DATABASE rbac_admin DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6. 初始化数据

```bash
python scripts/init_db.py
```

### 7. 启动服务

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 8. 访问系统

- API 地址：http://localhost:8000
- Swagger 文档：http://localhost:8000/docs
- ReDoc 文档：http://localhost:8000/redoc

### 默认账号

| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin | admin123 | 超级管理员 |

> 首次登录后请立即修改默认密码！

## API 接口

### 认证接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/v1/auth/login | 用户登录 |
| GET | /api/v1/auth/captcha | 获取验证码 |
| GET | /api/v1/auth/me | 获取当前用户信息 |

### 用户管理

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | /api/v1/users | 用户列表 | user:list |
| GET | /api/v1/users/{id} | 用户详情 | user:list |
| POST | /api/v1/users | 创建用户 | user:create |
| PUT | /api/v1/users/{id} | 更新用户 | user:update |
| DELETE | /api/v1/users/{id} | 删除用户 | user:delete |

### 角色管理

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | /api/v1/roles | 角色列表 | role:list |
| GET | /api/v1/roles/{id} | 角色详情 | role:list |
| POST | /api/v1/roles | 创建角色 | role:create |
| PUT | /api/v1/roles/{id} | 更新角色 | role:update |
| DELETE | /api/v1/roles/{id} | 删除角色 | role:delete |

### 权限管理

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | /api/v1/permissions | 权限列表 | perm:list |
| GET | /api/v1/permissions/{id} | 权限详情 | perm:list |
| POST | /api/v1/permissions | 创建权限 | perm:create |
| PUT | /api/v1/permissions/{id} | 更新权限 | perm:update |
| DELETE | /api/v1/permissions/{id} | 删除权限 | perm:delete |

### 菜单管理

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | /api/v1/menus/tree | 菜单树 | 登录即可 |
| GET | /api/v1/menus/{id} | 菜单详情 | menu:list |
| POST | /api/v1/menus | 创建菜单 | menu:create |
| PUT | /api/v1/menus/{id} | 更新菜单 | menu:update |
| DELETE | /api/v1/menus/{id} | 删除菜单 | menu:delete |

## Linux 部署

### 使用部署脚本（推荐）

```bash
chmod +x deploy.sh
./deploy.sh
```

### 使用 systemd 管理服务

创建服务文件 `/etc/systemd/system/rbac_admin.service`：

```ini
[Unit]
Description=RBAC Admin API Service
After=network.target mysql.service redis.service

[Service]
Type=simple
User=www
WorkingDirectory=/opt/rbac_admin
Environment="PATH=/opt/rbac_admin/venv/bin"
ExecStart=/opt/rbac_admin/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable rbac_admin
sudo systemctl start rbac_admin
```

### 使用 Nginx 反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 统一响应格式

所有接口返回以下 JSON 格式：

```json
{
    "code": 200,
    "message": "success",
    "data": {}
}
```

| code | 说明 |
|------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 429 | 请求过于频繁 |
| 500 | 服务器内部错误 |

## License

MIT