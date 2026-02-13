# Multi-stage Dockerfile for FamilyMan UI (Next.js + FastAPI)
# Stage 1: Build Next.js application
FROM node:20-alpine AS nextjs-builder

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY package-lock.json* ./
COPY pnpm-lock.yaml* ./
COPY yarn.lock* ./

# Install dependencies (support multiple package managers)
# Skip postinstall scripts since we handle agent setup separately
RUN if [ -f pnpm-lock.yaml ]; then \
        npm install -g pnpm && pnpm install --frozen-lockfile --ignore-scripts; \
    elif [ -f yarn.lock ]; then \
        yarn install --frozen-lockfile --ignore-scripts; \
    else \
        npm ci --ignore-scripts; \
    fi

# Copy application source
COPY . .

# Build Next.js application
RUN npm run build

# Stage 2: Setup Python agent
FROM python:3.12-slim AS python-builder

WORKDIR /app/agent

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy agent files
COPY agent/pyproject.toml agent/uv.lock* ./

# Install uv for faster Python package installation
RUN pip install uv

# Install Python dependencies
RUN uv pip install --system --no-cache -r pyproject.toml

# Stage 3: Production image with both services
FROM python:3.12-slim

WORKDIR /app

# Install Node.js in the Python image
RUN apt-get update && apt-get install -y \
    curl \
    netcat-openbsd \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=python-builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=python-builder /usr/local/bin /usr/local/bin

# Copy Next.js build from builder
COPY --from=nextjs-builder /app/.next ./.next
COPY --from=nextjs-builder /app/node_modules ./node_modules
COPY --from=nextjs-builder /app/package.json ./package.json
COPY --from=nextjs-builder /app/public ./public
COPY --from=nextjs-builder /app/next.config.ts ./next.config.ts

# Copy source files needed at runtime
COPY src ./src
COPY agent ./agent

# Copy startup script
COPY scripts/docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Expose ports for Next.js (3000) and FastAPI (8001)
EXPOSE 3000 8001

# Environment variables (will be overridden by k8s)
ENV NODE_ENV=production
ENV PORT=3000
ENV PYTHON_PORT=8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:3000/ || exit 1

# Run both services
ENTRYPOINT ["docker-entrypoint.sh"]
