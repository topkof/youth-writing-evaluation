# ============================================
# 前端生产镜像 - 极简优化版
# 镜像大小：~150MB
# ============================================

# Stage 1: 安装依赖
FROM node:18-alpine AS deps

WORKDIR /app

COPY frontend/package*.json ./
RUN npm ci

# Stage 2: 构建
FROM node:18-alpine AS builder

WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY frontend/ .

ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

# Stage 3: 生产镜像 - 使用 serve 托管静态文件
FROM node:18-alpine AS production

WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV NPM_CONFIG_LOGLEVEL=warn

# 安装 serve 用于托管静态文件
RUN npm install -g serve && npm cache clean --force

# 复制构建产物
COPY --from=builder /app/.next/standalone ./server
COPY --from=builder /app/.next/static ./static
COPY --from=builder /app/public ./public

# 创建非 root 用户
RUN addgroup -g 1001 nodejs && \
    adduser -u 1001 -G nodejs -s /bin/sh -D nextjs && \
    chown -R nextjs:nodejs /app
USER nextjs

EXPOSE 3000

CMD ["serve", "-s", "server", "-l", "3000"]
