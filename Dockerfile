# Gunakan Python 3.11 slim (ringan)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install sistem dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Copy project files
COPY pyproject.toml uv.lock ./
COPY src/ ./src/
COPY data/ ./data/

# Install dependencies menggunakan UV
RUN uv sync --frozen --no-dev

# Expose port Streamlit
EXPOSE 8501

# Environment variables
ENV PYTHONPATH=/app
ENV GEMINI_API_KEY=${GEMINI_API_KEY}

# Jalankan Streamlit
CMD ["uv", "run", "streamlit", "run", "src/main.py", "--server.port=8501", "--server.address=0.0.0.0"]