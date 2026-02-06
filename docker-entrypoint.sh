#!/bin/sh
set -e

echo "Starting Youth Writing Evaluation System..."

# 创建必要目录
mkdir -p /var/log/youth-writing
mkdir -p /app/uploads

# 设置权限
chown -R appuser:appgroup /app /var/log/youth-writing 2>/dev/null || true

# 等待数据库就绪
echo "Waiting for database..."
until python3 -c "import psycopg2; psycopg2.connect('host=postgres user=postgres dbname=youth_writing')" 2>/dev/null; do
    echo "Database not ready, waiting..."
    sleep 2
done
echo "Database is ready!"

# 初始化数据库
echo "Initializing database..."
cd /app/backend
python3 -m alembic upgrade head 2>/dev/null || true

# 启动前端静态文件服务（在后台）
echo "Starting frontend static server..."
serve -s /app/frontend-server -l 8080 &
FRONTEND_PID=$!

# 启动后端 API 服务
echo "Starting FastAPI backend..."
cd /app/backend
exec python3 main.py
