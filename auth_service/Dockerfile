# Load base image, Python 3.11
FROM python:3.11-slim

# Ignore files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code

# app
WORKDIR /code 

# Cleanup
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code

EXPOSE 4500

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "4500"]