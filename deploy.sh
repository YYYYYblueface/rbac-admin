#!/bin/bash
# =========================================
# RBAC Admin 部署脚本 (CentOS 10)
# =========================================

set -e

echo "========================================"
echo "  RBAC Admin 系统部署脚本"
echo "========================================"

# 检查 Python 版本
echo "[1/6] 检查 Python 环境..."
python3 --version || { echo "请先安装 Python 3.10+"; exit 1; }

# 创建虚拟环境
echo "[2/6] 创建虚拟环境..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# 安装依赖
echo "[3/6] 安装 Python 依赖..."
pip install --upgrade pip
pip install -r requirements.txt

# 配置环境变量
echo "[4/6] 配置环境变量..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "  请编辑 .env 文件，修改数据库和 Redis 配置"
    echo "  然后重新运行此脚本"
    exit 1
fi

# 初始化数据库
echo "[5/6] 初始化数据库..."
python scripts/init_db.py

# 启动服务
echo "[6/6] 启动服务..."
echo "  启动命令: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
echo ""
echo "========================================"
echo "  部署完成！"
echo "  访问地址: http://localhost:8000"
echo "  API 文档: http://localhost:8000/docs"
echo "  默认账号: admin / admin123"
echo "========================================"