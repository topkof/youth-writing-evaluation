# 青少年写作质量评测系统 - 宝塔面板部署指南

## 一、环境准备

### 1.1 服务器要求

| 配置项 | 最低要求 | 推荐配置 |
|--------|----------|----------|
| CPU | 1 核 | 2 核及以上 |
| 内存 | 2 GB | 4 GB 及以上 |
| 硬盘 | 20 GB | 50 GB 及以上 |
| 带宽 | 1 Mbps | 5 Mbps 及以上 |
| 操作系统 | CentOS 7+ / Ubuntu 18+ / Debian 10+ |

### 1.2 安装宝塔面板

```bash
# CentOS 系统
yum install -y wget && wget -O install.sh http://download.bt.cn/install/install_6.0.sh && sh install.sh

# Ubuntu/Debian 系统
wget -O install.sh http://download.bt.cn/install/install-ubuntu_6.0.sh && sudo bash install.sh
```

安装完成后，记录面板地址、用户名和密码。

### 1.3 安装必要软件

登录宝塔面板，在「软件商店」中安装：

1. **Nginx** - Web 服务器（推荐 1.22 版本）
2. **PM2 管理器** - Node.js 进程管理
3. **Python 3.9+** - Python 环境（如果未预装）
4. **phpMyAdmin** - 数据库管理（可选）

## 二、部署后端服务

### 2.1 创建站点

1. 进入宝塔面板 → 「网站」 → 「添加站点」
2. 填写配置：
   - 域名：`api.yourdomain.com`
   - 根目录：`/www/wwwroot/youth-writing/backend`
   - PHP 版本：选择「纯静态」

### 2.2 上传项目代码

```bash
# 连接到服务器
ssh root@your_server_ip

# 进入后端目录
cd /www/wwwroot/youth-writing/backend

# 上传项目代码（可通过 Git 或 FTP 上传）
git clone https://your-repo-url.git .

# 安装依赖
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2.3 配置环境变量

在 `/www/wwwroot/youth-writing/backend/` 目录下创建 `.env` 文件：

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑配置
vi .env
```

```env
# 数据库配置
DATABASE_URL=postgresql+asyncpg://your_db_user:your_db_password@localhost:5432/youth_writing

# Redis 配置
REDIS_HOST=localhost
REDIS_PORT=6379

# 安全配置
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# LLM 配置（根据实际情况修改）
LLM_DEFAULT_MODEL=gpt-4-turbo
OPENAI_API_KEY=sk-your-api-key

# OSS 配置（可选）
OSS_ENABLED=false
```

### 2.4 安装 PostgreSQL

1. 在宝塔面板「软件商店」中安装「PostgreSQL」
2. 创建数据库：
   ```bash
   # 连接到 PostgreSQL
   sudo -u postgres psql

   # 执行以下 SQL
   CREATE DATABASE youth_writing;
   CREATE USER your_db_user WITH PASSWORD 'your_db_password';
   GRANT ALL PRIVILEGES ON DATABASE youth_writing TO your_db_user;
   ALTER USER your_db_user CREATEDB;
   \q
   ```

3. 初始化数据库：
   ```bash
   cd /www/wwwroot/youth-writing/backend
   alembic upgrade head
   ```

### 2.5 使用 PM2 管理后端

1. 在宝塔面板「软件商店」中安装「PM2 管理器」
2. 进入 PM2 管理器 → 「添加项目」
3. 填写配置：
   - 项目名称：`youth-writing-backend`
   - 启动文件：`run.py`
   - 运行目录：`/www/wwwroot/youth-writing/backend`
   - 启动命令：`python main.py`
   - 运行用户：`www`

4. 创建 `/www/wwwroot/youth-writing/backend/run.py`：

```python
#!/usr/bin/env python
import uvicorn
from app.main import app

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        workers=1,
        access_log=True,
    )
```

5. 设置权限：
```bash
chmod +x run.py
chown -R www:www /www/wwwroot/youth-writing/backend
```

6. 在 PM2 中启动项目，确保状态为「运行中」

## 三、部署前端服务

### 3.1 创建站点

1. 进入宝塔面板 → 「网站」 → 「添加站点」
2. 填写配置：
   - 域名：`www.yourdomain.com`（主域名）
   - 根目录：`/www/wwwroot/youth-writing/frontend`
   - PHP 版本：选择「纯静态」

### 3.2 构建前端

```bash
# 在本地或服务器上构建
cd /www/wwwroot/youth-writing/frontend

# 修改 API 地址
# 编辑 next.config.js，将代理地址改为实际的 API 地址
# 或者直接构建后上传

# 构建生产版本
npm run build

# 构建产物在 .next 目录
```

### 3.3 上传并配置

1. 将构建产物上传到 `/www/wwwroot/youth-writing/frontend/`
2. 或者在服务器上直接构建：
```bash
# 安装 Node.js（使用 PM2 管理器安装）
# 安装依赖
npm install

# 构建
npm run build

# 设置输出目录为 out
# 修改 package.json：
# "start": "npm run build && npx serve out"
```

### 3.4 使用 PM2 启动前端

1. 在 PM2 管理器中添加项目：
   - 项目名称：`youth-writing-frontend`
   - 启动文件：`package.json` 中的 start 脚本
   - 运行目录：`/www/wwwroot/youth-writing/frontend`
   - 运行用户：`www`

2. 或使用 `npx serve out` 启动静态服务器

## 四、配置 Nginx 反向代理

### 4.1 进入 Nginx 配置

1. 宝塔面板 → 「网站」 → 点击站点右侧「设置」
2. 选择「反向代理」→ 「添加反向代理」

### 4.2 配置 API 代理

**代理名称**：`api_proxy`

**目标 URL**：`http://127.0.0.1:8000`

**发送域名**：`$host`

**高级配置**：
```nginx
location /api/ {
    proxy_pass http://127.0.0.1:8000/api/;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_read_timeout 300s;
    proxy_connect_timeout 75s;
}
```

### 4.3 配置前端代理

如果前端使用 Next.js 开发服务器：

**代理名称**：`frontend_proxy`

**目标 URL**：`http://127.0.0.1:3000`

**发送域名**：`$host`

## 五、配置 SSL 证书

### 5.1 申请免费证书

1. 宝塔面板 → 「网站」 → 点击站点 → 「SSL」
2. 选择「Let's Encrypt」
3. 勾选域名，申请证书
4. 开启「强制 HTTPS」

### 5.2 手动配置证书（如果有商业证书）

```nginx
server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;
    
    ssl_certificate /www/server/panel/vhost/cert/yourdomain.com/fullchain.pem;
    ssl_certificate_key /www/server/panel/vhost/cert/yourdomain.com/privkey.pem;
    ssl_session_timeout 5m;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:HIGH:!aNULL:!MD5:!RC4:!DHE;
    ssl_prefer_server_ciphers on;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 六、配置防火墙

### 6.1 开放端口

在宝塔面板「安全」→「防火墙」中开放：

| 端口 | 用途 |
|------|------|
| 80 | HTTP（临时） |
| 443 | HTTPS |
| 8000 | 后端服务（仅本地） |
| 3000 | 前端开发服务（仅本地） |

### 6.2 云服务器安全组

如果使用云服务器（如阿里云、腾讯云），需要在控制台开放：

- 80 端口
- 443 端口

## 七、系统监控

### 7.1 PM2 监控

通过 PM2 管理器可以查看：

- 进程状态
- CPU/内存使用
- 日志输出
- 重启/停止操作

### 7.2 配置开机自启

```bash
# 创建 systemd 服务
sudo vi /etc/systemd/system/youth-writing.service
```

```ini
[Unit]
Description=Youth Writing Evaluation Backend
After=network.target

[Service]
User=www
WorkingDirectory=/www/wwwroot/youth-writing/backend
Environment="PATH=/www/wwwroot/youth-writing/backend/venv/bin"
ExecStart=/www/wwwroot/youth-writing/backend/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# 启用服务
sudo systemctl enable youth-writing
sudo systemctl start youth-writing
```

## 八、常见问题处理

### 8.1 后端无法启动

```bash
# 检查端口是否被占用
netstat -tlnp | grep 8000

# 检查日志
pm2 logs youth-writing-backend

# 检查 Python 环境
source venv/bin/activate
python -c "import app.main; print('OK')"
```

### 8.2 数据库连接失败

```bash
# 测试数据库连接
sudo -u postgres psql -d youth_writing

# 检查数据库服务状态
systemctl status postgresql
```

### 8.3 静态文件不显示

1. 检查目录权限：
```bash
chmod -R 755 /www/wwwroot/youth-writing/frontend
chown -R www:www /www/wwwroot/youth-writing/frontend
```

2. 检查 Nginx 配置是否正确

### 8.4 CORS 跨域问题

在 `app/main.py` 中确保 CORS 配置正确：

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 九、定期维护

### 9.1 代码更新

```bash
cd /www/wwwroot/youth-writing/backend
git pull origin main

# 如果有数据库迁移
alembic upgrade head

# 重启服务
pm2 restart youth-writing-backend
```

### 9.2 日志清理

```bash
# 清理 PM2 日志
pm2 flush

# 清理 Nginx 日志
: > /www/server/nginx/logs/access.log
: > /www/server/nginx/logs/error.log
```

### 9.3 数据备份

在宝塔面板「计划任务」中添加备份任务：

- 备份数据库
- 备份项目文件
- 定期执行，建议每日备份

## 十、性能优化

### 10.1 后端优化

1. **增加工作进程数**：修改 `run.py` 中的 `workers` 参数
2. **开启 Gzip 压缩**：在 Nginx 配置中添加
3. **使用 Redis 缓存**：配置 Redis 缓存热点数据

### 10.2 数据库优化

1. 定期执行 `VACUUM ANALYZE`
2. 优化数据库连接池配置
3. 为常用查询添加索引

### 10.3 前端优化

1. 开启静态资源缓存
2. 使用 CDN 加速静态文件
3. 开启 Gzip 压缩

---

## 联系方式

如有问题，请检查：

1. 后端日志：`pm2 logs youth-writing-backend`
2. Nginx 错误日志：`/www/server/nginx/logs/error.log`
3. 数据库日志：`/var/log/postgresql/postgresql*.log`
