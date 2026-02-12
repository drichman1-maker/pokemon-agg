
# 1. Base Image
FROM python:3.9-slim

# 2. Env Vars
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# 3. Workdir
WORKDIR /app

# 4. Dependencies
COPY backend/pyproject.toml /app/
# Convert pyproject.toml to requirements or just install directly if using uv/poetry.
# For simplicity in this scaffold, we'll assume a requirements generation step or direct pip install if compliant.
# Here we'll install manually based on the pyproject we defined.
RUN pip install --no-cache-dir fastapi uvicorn pydantic-settings sqlalchemy asyncpg boto3 httpx python-multipart sendgrid apscheduler slowapi

# 5. Application Code
COPY backend/app /app/app

# 6. User (Security)
RUN adduser --disabled-password --gecos '' backend_user
USER backend_user

# 7. Entrypoint
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
