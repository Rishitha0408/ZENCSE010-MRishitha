# STAGE 1: Build dependencies
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build tools if any (not needed for current requirements, but good practice)
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# STAGE 2: Runtime
FROM python:3.12-slim AS runtime

WORKDIR /app

# Copy only the installed packages from the builder stage
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app/requirements.txt .

# Ensure scripts in .local are in PATH
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

# Expose port and run
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
