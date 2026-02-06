# 青少年写作质量评测系统

<div align="center">

[![GitHub stars](https://img.shields.io/github/stars/yourusername/youth-writing-evaluation)](https://github.com/yourusername/youth-writing-evaluation)
[![GitHub issues](https://img.shields.io/github/issues/yourusername/youth-writing-evaluation)](https://github.com/yourusername/youth-writing-evaluation/issues)
[![License](https://img.shields.io/github/license/yourusername/youth-writing-evaluation)](https://github.com/yourusername/youth-writing-evaluation/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![Node](https://img.shields.io/badge/node-18-green)](https://nodejs.org/)

**面向小学阶段青少年的写作质量智能评测平台**

[功能特性](#功能特性) • [技术栈](#技术栈) • [快速开始](#快速开始) • [API 文档](#api-文档) • [部署指南](#部署指南)

</div>

---

## 项目简介

青少年写作质量评测系统是一个面向小学阶段（1-6年级）青少年的写作质量智能评测平台。系统支持全部写作类型（记叙文、议论文、说明文、读后感、游记、书信、诗歌等），提供完整的评测报告，包括分数评级、各维度评分、改进建议和范文对比，帮助青少年提升写作能力。

### 核心价值

- **智能评测**：基于大语言模型的自动化作文评分系统
- **因材施教**：根据不同年级自动调整评分标准
- **全面分析**：从内容、结构、语言、规范、创意五个维度深入分析
- **成长追踪**：记录历史评测数据，可视化展示进步曲线
- **专业指导**：提供针对性的改进建议和学习方向

---

## 功能特性

### 评分维度体系

系统采用五个核心评分维度进行全面评估：

| 维度 | 分值范围 | 评估内容 |
|------|----------|----------|
| 内容主题 | 0-30 分 | 主题明确性、内容充实度、思想深度 |
| 结构组织 | 0-20 分 | 段落清晰度、逻辑连贯性、开头结尾质量 |
| 语言表达 | 0-25 分 | 用词准确性、句式丰富度、表达流畅性 |
| 书写规范 | 0-15 分 | 错别字数量、标点使用正确性、格式规范性 |
| 创意特色 | 0-10 分 | 独特视角、创新表达、个人风格 |

### 年级差异化评分

根据不同年级自动调整评分权重，真正做到因材施教：

```
一年级/二年级：侧重基础表达能力
三年级：过渡阶段，逐步提升要求
四年级/五年级：提高综合写作能力要求
六年级：接近初中水平，综合能力评估
```

### 写作类型识别

支持七种写作类型的自动识别与专项评分：

1. **记叙文** - 记人叙事、事件描述
2. **议论文** - 观点阐述、论证说理
3. **说明文** - 事物介绍、知识讲解
4. **读后感** - 阅读感受与思考
5. **游记** - 旅行见闻与感受
6. **书信** - 书信格式与情感表达
7. **诗歌** - 文学创作与表达

### 评测报告功能

- **总分评级**：优秀、良好、合格、待提高
- **维度分析**：各维度详细得分及评语
- **改进建议**：短期、中期、长期改进方向
- **范文对比**：同类型优秀范文对照分析
- **历史追踪**：进步曲线和统计分析

### 多模型支持

支持多种大语言模型服务商：

- OpenAI GPT-4 / GPT-3.5
- Anthropic Claude
- Google Gemini
- 百度文心一言
- 阿里通义千问
- 智谱清言
- 自定义 OpenAI 兼容 API

---

## 技术栈

### 后端技术

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.11+ | 运行时环境 |
| FastAPI | 0.109+ | Web 框架 |
| SQLAlchemy | 2.0+ | ORM |
| PostgreSQL | 15+ | 主数据库 |
| Redis | 7+ | 缓存、会话 |
| Alembic | 1.13+ | 数据库迁移 |
| Pydantic | 2.5+ | 数据验证 |

### 前端技术

| 技术 | 版本 | 用途 |
|------|------|------|
| Next.js | 14+ | React 框架 |
| React | 18+ | UI 库 |
| TypeScript | 5+ | 类型安全 |
| Tailwind CSS | 3.4+ | 样式框架 |
| shadcn/ui | - | 组件库 |
| Recharts | 2.10+ | 数据可视化 |
| TanStack Query | 5+ | 状态管理 |
| Axios | 1.6+ | HTTP 客户端 |

### 部署技术

| 技术 | 用途 |
|------|------|
| Docker | 容器化 |
| Docker Compose | 多容器编排 |
| Nginx | 反向代理 |
| PM2 | 进程管理 |
| Let's Encrypt | SSL 证书 |

---

## 项目结构

```
youth-writing-evaluation/
├── .monkeycode/                  # 项目规范文档
│   ├── specs/                    # 功能规格文档
│   │   └── youth-writing-evaluation-system/
│   │       ├── requirements.md    # 需求文档
│   │       ├── design.md          # 技术设计文档
│   │       └── tasklist.json     # 开发任务列表
│   └── rules/                     # 自动化规则
│
├── backend/                       # 后端项目
│   ├── app/                       # FastAPI 应用
│   │   ├── api/                   # API 路由
│   │   │   └── v1/
│   │   │       └── endpoints/     # 接口实现
│   │   ├── core/                  # 核心配置
│   │   ├── models/                # 数据模型
│   │   ├── schemas/               # Pydantic 模型
│   │   ├── services/              # 业务逻辑
│   │   │   ├── llm/              # LLM 服务
│   │   │   ├── scoring/           # 评分引擎
│   │   │   ├── essay/             # 作文服务
│   │   │   └── ...
│   │   └── utils/                 # 工具函数
│   ├── migrations/                 # 数据库迁移
│   ├── requirements.txt           # Python 依赖
│   ├── Dockerfile                 # Docker 构建文件
│   └── DEPLOY_BAOTA.md           # 宝塔部署指南
│
├── frontend/                      # 前端项目
│   ├── src/                       # 源代码
│   │   ├── app/                   # Next.js 页面
│   │   │   ├── page.tsx           # 首页
│   │   │   └── layout.tsx        # 布局
│   │   ├── components/            # React 组件
│   │   │   ├── ui/                # 基础组件
│   │   │   ├── essay-editor.tsx   # 作文编辑器
│   │   │   ├── score-card.tsx     # 评分卡片
│   │   │   └── radar-chart.tsx    # 雷达图
│   │   ├── lib/                   # 工具库
│   │   │   ├── api.ts             # API 客户端
│   │   │   └── utils.ts           # 工具函数
│   │   └── styles/                # 样式文件
│   ├── public/                    # 静态资源
│   ├── package.json              # Node 依赖
│   ├── Dockerfile                # Docker 构建文件
│   └── next.config.js            # Next.js 配置
│
├── docker-compose.yml           # Docker Compose 配置
├── nginx.conf                   # Nginx 配置
├── .env.example                 # 环境变量模板
├── README.md                   # 项目说明文档
└── README_DOCKER.md           # Docker 部署指南
```

---

## 快速开始

### 环境要求

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+

### 方式一：本地开发

#### 1. 克隆项目

```bash
git clone https://github.com/yourusername/youth-writing-evaluation.git
cd youth-writing-evaluation
```

#### 2. 后端配置

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置数据库和 API Key

# 初始化数据库
alembic upgrade head

# 启动后端
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 3. 前端配置

```bash
cd frontend

# 安装依赖
npm install

# 配置环境变量
# 创建 .env.local 文件

# 启动开发服务器
npm run dev
```

#### 4. 访问应用

- 前端应用：http://localhost:3000
- 后端 API：http://localhost:8000
- API 文档：http://localhost:8000/docs

### 方式二：Docker 部署

#### 1. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入必要配置
```

#### 2. 启动服务

```bash
# 构建并启动
docker compose up -d --build

# 查看日志
docker compose logs -f
```

#### 3. 验证部署

```bash
# 检查前端
curl http://localhost:3000

# 检查后端健康
curl http://localhost:8000/health
```

---

## API 文档

### 认证接口

```http
POST /api/v1/users/register
POST /api/v1/users/login
GET  /api/v1/users/profile
```

### 作文评测接口

```http
POST /api/v1/essays/evaluate      # 评测单篇作文
POST /api/v1/essays/batch-evaluate # 批量评测
GET  /api/v1/essays/result/{id}    # 获取评测结果
```

### 历史记录接口

```http
GET  /api/v1/history/list           # 获取历史列表
GET  /api/v1/history/progress/{user_id} # 进步曲线
GET  /api/v1/history/statistics/{user_id} # 统计数据
```

### 范文库接口

```http
GET  /api/v1/examples/list           # 范文列表
GET  /api/v1/examples/{id}          # 范文详情
```

### 模型配置接口

```http
GET  /api/v1/models/list            # 模型列表
POST /api/v1/models/add             # 添加模型
POST /api/v1/models/test            # 测试连接
```

> 完整 API 文档请访问：http://localhost:8000/docs (Swagger UI)

---

## 部署指南

### Docker 部署（推荐）

详细部署指南请参考 [README_DOCKER.md](./README_DOCKER.md)

```bash
# 开发环境
docker compose up -d

# 生产环境（包含 Nginx）
docker compose --profile production up -d
```

### 宝塔面板部署

详细部署指南请参考 [backend/DEPLOY_BAOTA.md](./backend/DEPLOY_BAOTA.md)

### 手动部署

1. **安装依赖软件**
   - Nginx
   - PostgreSQL
   - Redis
   - Node.js 18+
   - Python 3.11+

2. **配置后端**
   ```bash
   cd backend
   pip install -r requirements.txt
   cp .env.example .env
   alembic upgrade head
   ```

3. **配置前端**
   ```bash
   cd frontend
   npm install
   npm run build
   ```

4. **配置 Nginx**
   - 复制 nginx.conf 到 Nginx 配置目录
   - 配置 SSL 证书

5. **启动服务**
   - 使用 PM2 或 systemd 管理后端进程
   - 配置 Nginx 反向代理

---

## 配置说明

### 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `DATABASE_URL` | 是 | PostgreSQL 连接字符串 |
| `SECRET_KEY` | 是 | JWT 签名密钥 |
| `OPENAI_API_KEY` | 否 | OpenAI API Key |
| `REDIS_HOST` | 否 | Redis 主机 |
| `REDIS_PORT` | 否 | Redis 端口 |

### 数据库配置

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/youth_writing
```

### LLM 配置

```env
LLM_DEFAULT_MODEL=gpt-4-turbo
OPENAI_API_KEY=sk-your-api-key
```

---

## 测试

### 后端测试

```bash
cd backend

# 运行所有测试
pytest

# 运行覆盖率报告
pytest --cov=app --cov-report=html
```

### 前端测试

```bash
cd frontend

# 运行单元测试
npm test

# 运行 E2E 测试
npm run test:e2e
```

---

## 贡献指南

1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 开发规范

- Python 代码遵循 PEP 8，使用 Black 格式化
- JavaScript/TypeScript 代码遵循 ESLint 规则
- Git 提交信息遵循 Conventional Commits 规范
- 所有新功能需要添加对应测试

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v2.0.0 | 2026-02-06 | 初始版本发布 |

---

## 许可证

本项目采用 MIT License 开源许可证。

---

## 联系方式

- 项目地址：https://github.com/yourusername/youth-writing-evaluation
- Issue：https://github.com/yourusername/youth-writing-evaluation/issues
- 邮箱：contact@example.com

---

<div align="center">

**用 AI 赋能青少年写作教育**

</div>
