FROM python:3.11-slim

WORKDIR /app

# Copy requirements from apps/backend
COPY ./apps/backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy both backend and ml_engine into the container
COPY ./apps/backend ./apps/backend
COPY ./apps/ml_engine ./apps/ml_engine

# Set PYTHONPATH to root and backend so imports resolve correctly
ENV PYTHONPATH="/app:/app/apps/backend"

EXPOSE 8000

# Start command
CMD ["uvicorn", "apps.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
