# Use Python 3.14 slim image as base
FROM python:3.14-slim

# Install UV - the fast Python package installer
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy dependency files first for better layer caching
COPY pyproject.toml ./

# Install dependencies using UV
# --system flag installs to system Python instead of creating a virtual environment
RUN uv pip install --system -r pyproject.toml

# Set Python path to include src directory
# Expects src/ and templates/ to be mounted at /app/src and /app/templates
ENV PYTHONPATH=/app/src

# Set the entrypoint to the CLI
ENTRYPOINT ["python", "-m", "ksg.main"]

# Default command (can be overridden)
CMD ["--help"]
