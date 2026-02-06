# 青少年写作质量评测系统 - Docker 部署指南

## 目录

- [简介](#简介)
- [架构概览](#架构概览)
- [镜像优化](#镜像优化)
- [快速开始](#快速开始)
- [生产部署](#生产部署)
- [服务说明](#服务说明)
- [监控和维护](#监控和维护)
- [故障排除](#故障排除)

---

## 简介

本项目使用 Docker 容器化部署，包含以下服务：

- **PostgreSQL 15** - 主数据库
- **Redis 7** - 缓存和会话存储
- **FastAPI 后端** - API 服务
- **Next.js 前端** - Web 应用
- **Nginx** - 反向代理（生产环境）

---

## 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                        用户请求                              │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Nginx (80/443)                                           │
│  ├── 反向代理前端 -> frontend:3000                         │
│  └── 反向代理 API -> backend:8000                          │
└─────────────────────────┬───────────────────────────────────┘
                          │
              ┌──────────┴──────────┐
              ▼                      ▼
┌─────────────────────┐    ┌─────────────────────┐
│  Frontend (:3000)   │    │  Backend (:8000)    │
│  Next.js 14         │    │  FastAPI + Uvicorn  │
│  Node.js 18 Alpine  │    │  Python 3.11 Slim   │
└─────────────────────┘    └─────────────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    ▼                 ▼                 ▼
          ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
          │  Redis (:6379) │ │ PostgreSQL      │ │   上传文件      │
          │  缓存          │ │ (:5432)         │ │   持久化卷      │
          └─────────────────┘ └─────────────────┘ └─────────────────┘
```

---

## 镜像优化

本项目采用以下优化策略将镜像体积降到最低：

### 后端优化

| 优化策略 | 说明 | 效果 |
|----------|------|------|
| **多阶段构建** | 分离编译依赖和运行时依赖 | 减少 ~300MB |
| **Python Slim 镜像** | 使用 slim 版本，不含开发工具 | 减少 ~500MB |
| **依赖缓存** | 只在依赖变更时重新安装 | 加快构建 |
| **非 root 用户** | 提高安全性 | - |
| **健康检查** | 容器自检机制 | 提高可用性 |

### 前端优化

| 优化策略 | 说明 | 效果 |
|----------|------|------|
| **Alpine 镜像** | 最小的 Node.js 镜像 | 减少 ~800MB |
| **standalone 输出** | Next.js 独立输出 | 减少 ~100MB |
| **依赖缓存** | 分离依赖安装阶段 | 加快构建 |
| **静态资源优化** | Gzip 压缩、缓存头 | 提高性能 |

### 镜像大小对比

```
优化前：
├── Python:3.11         ~1.1 GB
├── Node:18            ~1.2 GB
└── 总计               ~2.3 GB

优化后：
├── Python:3.11-slim   ~150 MB
├── Node:18-alpine     ~180 MB
└── 总计               ~330 MB

减少约 85%
```

---

## All-in-One 合并部署模式

### 简介

All-in-One 模式将前端静态文件和后端 API 合并为一个 Docker 镜像，通过 Nginx 同时提供静态文件服务和 API 反向代理。

### 架构图

```
┌─────────────────────────────────────────────────────────────┐
│                        用户请求                              │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Nginx (:8080)                                            │
│  ├── 静态文件 -> /var/www/standalone                     │
│  └── API -> localhost:8000 (FastAPI)                      │
└─────────────────────────┬───────────────────────────────────┘
                          │
              ┌──────────┴──────────┐
              ▼                      ▼
┌─────────────────────┐    ┌─────────────────────┐
│  FastAPI (:8000)   │    │   Nginx (:8080)    │
│  Python 3.11       │    │  Alpine            │
│  + Nginx           │    │  前端静态文件       │
└─────────────────────┘    └─────────────────────┘
              │
              ▼
┌─────────────────────┐
│  PostgreSQL/Redis  │
└─────────────────────┘
```

### 镜像大小对比

| 模式 | 镜像数量 | 单镜像大小 | 总大小 | 启动容器数 |
|------|----------|-----------|--------|-----------|
| 分离模式 | 2 | ~180MB | ~360MB | 3 (frontend+backend+nginx) |
| All-in-One | 1 | ~200MB | ~200MB | 1 |
| **节省** | 50% | - | **44%** | **67%** |

### 快速开始

```bash
# 启动 All-in-One 模式
docker compose --profile allinone up -d --build

# 访问应用
curl http://localhost:8080

# 查看日志
docker compose logs -f allinone
```

### 使用预构建镜像

```bash
# 拉取并运行
docker run -d \
  --name youth-writing-allinone \
  -p 8080:8080 \
  -e POSTGRES_PASSWORD=your_password \
  -e SECRET_KEY=your-secret-key \
  ghcr.io/topkof/youth-writing-evaluation/allinone:latest
```

### 端口说明

| 模式 | 端口 | 用途 |
|------|------|------|
| 分离模式 | 3000 | 前端 |
| 分离模式 | 8000 | 后端 API |
| All-in-One | 8080 | 前端 + API 统一入口 |
| 生产环境 | 80/443 | Nginx 反向代理 |

### 优缺点对比

| 特性 | 分离模式 | All-in-One 模式 |
|------|----------|-----------------|
| 镜像大小 | 较大 (~360MB) | 较小 (~200MB) |
| 启动时间 | 较慢 (3个容器) | 较快 (1个容器) |
| 资源占用 | 较高 | 较低 |
| 扩展性 | 前后端独立扩展 | 整体扩展 |
| 适用场景 | 生产环境 | 开发/测试/小规模部署 |

### 选择建议

- **开发/测试**：推荐 All-in-One，部署简单
- **小规模生产**：推荐 All-in-One，资源占用低
- **大规模/高并发**：推荐分离模式，支持独立扩展
- **微服务架构**：推荐分离模式，便于独立更新

---

---

## 快速开始

### 1. 环境准备

```bash
# 确保已安装 Docker 和 Docker Compose
docker --version        # Docker 24.0+
docker compose version  # v2.20+

# 创建项目目录
mkdir youth-writing
cd youth-writing
```

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑配置（必需修改以下项）
vim .env
```

**必须修改的配置项：**

```env
# 数据库密码（强密码建议）
POSTGRES_PASSWORD=YourStrongPassword123!

# JWT 密钥（32位以上随机字符串）
SECRET_KEY=your-super-secret-key-at-least-32-characters-long

# OpenAI API Key（可选，用于 AI 评分功能）
OPENAI_API_KEY=sk-your-api-key
```

### 3. 启动服务

```bash
# 构建并启动所有服务（后台运行）
docker compose up -d --build

# 查看启动状态
docker compose ps

# 查看日志
docker compose logs -f
```

### 4. 验证部署

```bash
# 检查前端
curl http://localhost:3000

# 检查后端健康
curl http://localhost:8000/health

# 检查 API 文档
open http://localhost:8000/docs
```

**预期输出：**

```json
{
  "status": "healthy",
  "version": "2.0.0"
}
```

---

## 生产部署

### 1. 配置 SSL 证书

```bash
# 创建 SSL 证书目录
mkdir -p ssl

# 使用 Let's Encrypt（需要域名已解析）
certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com

# 复制证书
cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ssl/
cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ssl/
```

### 2. 修改 Nginx 配置

编辑 `nginx.conf`，取消 HTTPS 服务器块的注释：

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    # ... 其他配置
}

# HTTP 重定向到 HTTPS
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

### 3. 启动生产环境

```bash
# 包含 Nginx 的完整部署
docker compose --profile production up -d --build
```

### 4. 配置防火墙

```bash
# Ubuntu UFW
sudo ufw allow 80
sudo ufw allow 443

# 云服务器安全组
# 在阿里云/腾讯云控制台开放 80、443 端口
```

---

## 服务说明

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `POSTGRES_PASSWORD` | - | **必填** PostgreSQL 密码 |
| `SECRET_KEY` | - | **必填** JWT 签名密钥 |
| `OPENAI_API_KEY` | - | OpenAI API Key（AI 评分功能） |
| `LLM_DEFAULT_MODEL` | `gpt-4-turbo` | 默认 LLM 模型 |
| `MAX_FILE_SIZE` | `10485760` | 最大上传文件大小（字节） |
| `OSS_ENABLED` | `false` | 是否启用阿里云 OSS |

### 端口映射

| 服务 | 内部端口 | 外部端口 | 说明 |
|------|----------|----------|------|
| PostgreSQL | 5432 | 5432 | 仅本地访问 |
| Redis | 6379 | 6379 | 仅本地访问 |
| Backend | 8000 | 8000 | API 服务 |
| Frontend | 3000 | 3000 | Web 应用 |
| All-in-One | 8080 | 8080 | 前端 + API 统一入口 |
| Nginx | 80/443 | 80/443 | 反向代理 |

### 数据持久化

```yaml
volumes:
  postgres_data:    # PostgreSQL 数据
  redis_data:       # Redis 数据
  backend_uploads:  # 上传文件
```

**备份命令：**

```bash
# 备份 PostgreSQL
docker compose exec postgres pg_dump -U postgres youth_writing > backup.sql

# 备份 Redis
docker compose exec redis redis-cli BGSAVE

# 备份上传文件
docker run --rm -v youth-writing_backend_uploads:/data -v $(pwd):/backup alpine tar czf /backup/uploads.tar.gz -C /data .
```

---

## 监控和维护

### 健康检查

```bash
# 检查所有服务状态
docker compose ps

# 检查容器健康状态
docker compose exec backend python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
```

### 日志查看

```bash
# 实时日志
docker compose logs -f

# 指定服务日志
docker compose logs -f backend
docker compose logs -f frontend

# 最近 100 行日志
docker compose logs --tail 100
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
# 拉取最新代码
git pull origin main

# 重新构建并启动
docker compose up -d --build

# 清理旧镜像
docker image prune -f
```

### 数据库迁移

```bash
# 查看当前迁移状态
docker compose exec backend alembic current

# 升级数据库
docker compose exec backend alembic upgrade head

# 创建新迁移
docker compose exec backend alembic revision -m "描述变更"
```

---

## 故障排除

### 1. 后端无法启动

```bash
# 检查端口占用
lsof -i :8000

# 查看详细错误
docker compose logs backend

# 常见原因：
# - DATABASE_URL 配置错误
# - PostgreSQL 未启动
# - 端口已被占用
```

### 2. 数据库连接失败

```bash
# 测试数据库连接
docker compose exec backend python -c "import asyncio; from app.db.session import engine; asyncio.run(engine.connect())"

# 检查 PostgreSQL 日志
docker compose logs postgres

# 解决方案：
# 1. 确保 POSTGRES_PASSWORD 与环境变量一致
# 2. 等待 PostgreSQL 完全启动（健康检查通过）
```

### 3. 前端 502 错误

```bash
# 检查前端日志
docker compose logs frontend

# 检查 Nginx 配置
docker compose exec nginx nginx -t

# 解决方案：
# 1. 确保前端容器正在运行
# 2. 检查 Nginx 反向代理配置
```

### 4. All-in-One 模式 502 错误

```bash
# 检查 allinone 日志
docker compose logs allinone

# 检查 Nginx 和 FastAPI 状态
docker compose exec allinone ps aux

# 解决方案：
# 1. 确保 PostgreSQL 和 Redis 健康检查通过
# 2. 检查端口 8080 是否被占用
# 3. 查看 FastAPI 日志确认后端启动成功
```

### 5. 文件上传失败

```bash
# 检查上传目录权限
docker compose exec backend ls -la /app/uploads

# 解决方案：
# 1. 确保 backend_uploads 卷已正确挂载
# 2. 检查 MAX_FILE_SIZE 配置
# 3. 检查 Nginx client_max_body_size 配置
```

### 5. CORS 跨域错误

在浏览器控制台查看错误，解决方案：

```python
# 确保 CORS 配置包含前端域名
# backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 6. 内存不足

```bash
# 查看内存使用
free -m

# 优化建议：
# 1. PostgreSQL: max_connections 调小
# 2. Redis: maxmemory 限制
# 3. 考虑增加服务器内存
```

---

## Docker 镜像构建单独使用

### 只构建后端镜像

```bash
cd backend
docker build -t youth-writing-backend .
docker run -d -p 8000:8000 --env-file ../.env youth-writing-backend
```

### 只构建前端镜像

```bash
cd frontend
docker build -t youth-writing-frontend .
docker run -d -p 3000:3000 -e API_URL=http://backend:8000 youth-writing-frontend
```

---

## 相关文档

- [宝塔面板部署指南](./backend/DEPLOY_BAOTA.md)
- [API 文档](http://localhost:8000/docs)
- [项目需求文档](./.monkeycode/specs/youth-writing-evaluation-system/requirements.md)
- [技术设计文档](./.monkeycode/specs/youth-writing-evaluation-system/design.md)
