# Use official Python lightweight image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies (required for some Python packages like psycopg2)
RUN apt-get update && apt-get install -y libpq-dev gcc

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run the application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
