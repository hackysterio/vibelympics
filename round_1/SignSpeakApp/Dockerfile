# Stage 1: Build the application using Chainguard Node
FROM cgr.dev/chainguard/node:latest AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install all dependencies (including devDependencies for build)
RUN npm ci

# Copy source code
COPY . .

# Build the frontend (creates dist/public with static files)
RUN npm run build

# Stage 2: Serve with Chainguard nginx
FROM cgr.dev/chainguard/nginx:latest

# Copy built static files to nginx html directory
COPY --from=builder /app/dist/public /usr/share/nginx/html

# Copy custom nginx config for SPA routing
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Chainguard nginx runs on port 8080 by default (non-root)
EXPOSE 8080
