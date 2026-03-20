# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
# Increase timeout to 1000 seconds to handle slow connections
RUN pip install --default-timeout=1000 --upgrade pip && pip install --default-timeout=1000 -r requirements.txt

# Copy project
COPY . /app/

# The command to run the application is handled by docker-compose
