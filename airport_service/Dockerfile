# Use lightweight Python image
FROM python:3.11-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy requirements first (cache layer)
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose port (matches your previous script)
EXPOSE 5300

# Run Uvicorn directly
CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "5300"]
