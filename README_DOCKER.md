# 青少年写作质量评测系统 - Docker 部署指南

## 目录

- [简介](#简介)
- [架构概览](#架构概览)
- [部署模式](#部署模式)
- [镜像优化](#镜像优化)
- [快速开始](#快速开始)
- [生产部署](#生产部署)
- [监控和维护](#监控和维护)
- [故障排除](#故障排除)

---

## 简介

本项目使用 Docker 容器化部署，包含以下服务：

- **PostgreSQL 15** - 主数据库
- **Redis 7** - 缓存和会话存储
- **FastAPI 后端** - API 服务（端口 8000）
- **Next.js 前端** - Web 应用（端口 3000）

**注意**：本项目不内置 Nginx 反向代理，请在部署环境手动配置。

---

## 架构概览

### 分离部署模式

```
┌─────────────────────────────────────────────────┐
│                   用户请求                         │
└────────────────────┬──────────────────────────┘
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│ 前端 (:3000)    │    │ 后端 (:8000)    │
│ Next.js 静态    │    │ FastAPI API    │
└────────┬────────┘    └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     ▼
         ┌───────────────────────┐
         │   PostgreSQL / Redis  │
         └───────────────────────┘
```

### All-in-One 合并模式

```
┌─────────────────────────────────────────────────┐
│                   用户请求                         │
└────────────────────┬──────────────────────────┘
                     ▼
         ┌───────────────────────┐
         │  All-in-One (:8080)  │
         │  ┌─────────────────┐  │
         │  │ 前端静态 (+API)  │  │
         │  └─────────────────┘  │
         └───────────┬───────────┘
                     ▼
         ┌───────────────────────┐
         │   PostgreSQL / Redis  │
         └───────────────────────┘
```

---

## 部署模式

### 模式 1：分离部署（推荐生产）

- **后端**：`ghcr.io/topkof/youth-writing-evaluation/backend:latest`
- **前端**：`ghcr.io/topkof/youth-writing-evaluation/frontend:latest`
- **端口**：前端 3000，后端 8000
- **适用**：生产环境，需要手动配置 Nginx 反向代理

### 模式 2：All-in-One 合并

- **镜像**：`ghcr.io/topkof/youth-writing-evaluation/allinone:latest`
- **端口**：8080
- **适用**：开发测试、小规模部署

### 模式 3：手动部署

- 分别运行后端和前端容器
- 完全独立管理
- **适用**：需要精细控制的场景

---

## 镜像优化

### 后端优化

| 优化策略 | 说明 | 效果 |
|----------|------|------|
| 多阶段构建 | 分离编译依赖和运行时依赖 | 减少 ~300MB |
| Python Slim | 使用 slim 版本，不含开发工具 | 减少 ~500MB |
| 最小依赖 | 只安装 libpq5 运行时 | 减少 ~20MB |
| 依赖缓存 | 只在依赖变更时重新安装 | 加快构建 |

### 前端优化

| 优化策略 | 说明 | 效果 |
|----------|------|------|
| Alpine 镜像 | 最小的 Node.js 镜像 | 减少 ~800MB |
| standalone 输出 | Next.js 独立输出 | 减少 ~100MB |
| serve 托管 | 使用 serve 而非 Node.js 服务器 | 减少 ~30MB |
| 依赖缓存 | 分离依赖安装阶段 | 加快构建 |

### 镜像大小对比

| 镜像 | 优化前 | 优化后 | 节省 |
|------|--------|--------|------|
| 后端 | ~1.1 GB | ~120 MB | **89%** |
| 前端 | ~1.2 GB | ~150 MB | **87%** |
| All-in-One | - | ~180 MB | - |

---

## 快速开始

### 环境准备

```bash
# 安装 Docker 和 Docker Compose
# 确保已配置好 PostgreSQL 和 Redis
```

### 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑配置（必需）
vim .env
```

必需配置项：

```env
POSTGRES_PASSWORD=your_secure_password
SECRET_KEY=your-jwt-secret-key-at-least-32-chars
OPENAI_API_KEY=sk-your-api-key
```

### 启动服务

#### 方式 1：All-in-One 合并模式

```bash
# 启动
docker compose --profile allinone up -d

# 访问
curl http://localhost:8080
```

#### 方式 2：分离部署

```bash
# 启动后端
docker compose up backend -d

# 启动前端
docker compose --profile frontend up -d

# 访问
curl http://localhost:3000      # 前端
curl http://localhost:8000/docs # API 文档
```

### 验证部署

```bash
# 检查容器状态
docker compose ps

# 检查后端健康
curl http://localhost:8000/health

# 检查前端
curl http://localhost:3000
```

---

## 生产部署

### 1. 拉取镜像

```bash
# 拉取后端镜像
docker pull ghcr.io/topkof/youth-writing-evaluation/backend:latest

# 拉取前端镜像
docker pull ghcr.io/topkof/youth-writing-evaluation/frontend:latest

# 或拉取 All-in-One 镜像
docker pull ghcr.io/topkof/youth-writing-evaluation/allinone:latest
```

### 2. 配置环境变量

```bash
# 创建 .env 文件
vim .env
```

```env
POSTGRES_PASSWORD=your_secure_password
SECRET_KEY=your-jwt-secret-key
OPENAI_API_KEY=sk-your-api-key
DATABASE_URL=postgresql://user:pass@host:5432/youth_writing
REDIS_HOST=your-redis-host
REDIS_PORT=6379
CORS_ORIGINS=https://yourdomain.com
```

### 3. 手动配置 Nginx 反向代理

**示例 Nginx 配置**：

```nginx
# /etc/nginx/conf.d/youth-writing.conf

# 前端静态文件
server {
    listen 80;
    server_name yourdomain.com;

    # 前端静态文件
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# 后端 API
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket 支持（如需要）
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # API 文档
    location /docs {
        proxy_pass http://localhost:8000/docs;
    }

    location /redoc {
        proxy_pass http://localhost:8000/redoc;
    }
}
```

### 4. 启动服务

```bash
# 启动数据库（如果使用容器外数据库，跳过）
docker compose up -d postgres redis

# 启动后端
docker compose up backend -d

# 启动前端
docker compose --profile frontend up -d
```

### 5. 配置 HTTPS（推荐）

使用 Let's Encrypt：

```bash
certbot --nginx -d yourdomain.com -d api.yourdomain.com
```

---

## 监控和维护

### 健康检查

```bash
# 检查所有服务状态
docker compose ps

# 检查后端健康
docker compose exec backend python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
```

### 日志查看

```bash
# 实时日志
docker compose logs -f

# 指定服务日志
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f allinone
```

### 资源监控

```bash
# 查看容器资源使用
docker stats

# 查看磁盘使用
df -h
docker system df
```

### 更新部署

```bash
# 拉取最新镜像
docker compose pull

# 重新启动
docker compose up -d

# 清理旧镜像
docker image prune -f
```

### 数据备份

```bash
# 备份 PostgreSQL
docker compose exec postgres pg_dump -U postgres youth_writing > backup.sql

# 备份 Redis
docker compose exec redis redis-cli BGSAVE

# 备份上传文件
docker run --rm -v youth-writing_backend_uploads:/data -v $(pwd):/backup alpine tar czf /backup/uploads.tar.gz -C /data .
```

---

## 故障排除

### 1. 后端无法启动

```bash
# 检查端口占用
lsof -i :8000

# 查看日志
docker compose logs backend

# 常见原因
# - DATABASE_URL 配置错误
# - PostgreSQL 未启动
# - 端口已被占用
```

### 2. 数据库连接失败

```bash
# 测试数据库连接
docker compose exec backend python -c "import psycopg2; psycopg2.connect('host=postgres user=postgres dbname=youth_writing')"

# 检查 PostgreSQL 日志
docker compose logs postgres

# 解决方案
# 1. 确保 POSTGRES_PASSWORD 与环境变量一致
# 2. 等待 PostgreSQL 完全启动
```

### 3. 前端无法访问

```bash
# 检查前端日志
docker compose logs frontend

# 检查端口
docker compose exec frontend netstat -tlnp | grep 3000

# 解决方案
# 1. 确保前端容器正在运行
# 2. 检查端口映射
# 3. 检查 CORS 配置
```

### 4. All-in-One 模式问题

```bash
# 检查日志
docker compose logs allinone

# 检查进程
docker compose exec allinone ps aux

# 解决方案
# 1. 确保 PostgreSQL 和 Redis 健康检查通过
# 2. 检查端口 8080 是否被占用
# 3. 查看 FastAPI 日志确认后端启动成功
```

### 5. CORS 跨域错误

```bash
# 确保 CORS_ORIGINS 配置正确
# 在 .env 中设置
CORS_ORIGINS=https://yourdomain.com
```

### 6. 内存不足

```bash
# 查看内存使用
free -m

# 优化建议
# 1. PostgreSQL: max_connections 调小
# 2. Redis: maxmemory 限制
# 3. 考虑增加服务器内存
```

---

## Docker 镜像使用

### 单独运行后端

```bash
docker run -d \
  --name youth-writing-backend \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  -e REDIS_HOST=... \
  -e SECRET_KEY=... \
  ghcr.io/topkof/youth-writing-evaluation/backend:latest
```

### 单独运行前端

```bash
docker run -d \
  --name youth-writing-frontend \
  -p 3000:3000 \
  -e API_URL=http://your-backend:8000 \
  ghcr.io/topkof/youth-writing-evaluation/frontend:latest
```

### 运行 All-in-One

```bash
docker run -d \
  --name youth-writing-allinone \
  -p 8080:8080 \
  -e DATABASE_URL=postgresql://... \
  -e REDIS_HOST=redis \
  ghcr.io/topkof/youth-writing-evaluation/allinone:latest
```

---

## 相关文档

- [宝塔面板部署指南](./backend/DEPLOY_BAOTA.md)
- [API 文档](http://localhost:8000/docs)
- [项目需求文档](./.monkeycode/specs/youth-writing-evaluation-system/requirements.md)
- [技术设计文档](./.monkeycode/specs/youth-writing-evaluation-system/design.md)
