# Use lightweight Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy dependency list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire app code
COPY . .

# Environment variable to show logs immediately
ENV PYTHONUNBUFFERED=1

# Expose FastAPI’s port
EXPOSE 8000

# Default command to run the API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
