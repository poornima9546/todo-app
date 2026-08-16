# ==============================
# Stage 1: Build stage
# ==============================

FROM python:3.12-slim AS builder

# Set working directory
WORKDIR /build

# Copy requirements file
COPY app/requirements.txt .

# Create a virtual environment
RUN python -m venv /opt/venv

# Install Python dependencies into the virtual environment
RUN /opt/venv/bin/pip install --no-cache-dir --upgrade "pip==25.3" && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt


# ==============================
# Stage 2: Production stage
# ==============================

FROM python:3.12-slim

# Update Debian security packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Create a non-root user
RUN useradd --create-home --shell /bin/bash appuser

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy application files
COPY app/ .

# Use the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Application port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Switch to non-root user
USER appuser

# Start Flask application
CMD ["python", "app.py"]
