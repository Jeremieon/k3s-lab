# Stage 1 — builder
FROM python:3.11-slim AS builder

WORKDIR /app

# Install dependencies into a separate directory
# This layer is cached — only rebuilds when requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2 — runtime (lean final image)
FROM python:3.11-slim

WORKDIR /app

# Install curl for health checks and in-cluster debugging
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy application code
COPY main.py .

# Run as non-root user — production security requirement
RUN useradd -m -u 1001 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 80

# CMD runs uvicorn directly — no gunicorn wrapper needed for K8s
# K8s handles scaling via replicas, not gunicorn workers
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
