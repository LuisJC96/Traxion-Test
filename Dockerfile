# Use Ubuntu as base image
FROM ubuntu:latest

# Set environment variables to non-interactive (for installations)
ENV DEBIAN_FRONTEND=noninteractive

# Install prerequisites and add PPA for Python 3.12
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    software-properties-common \
    gnupg \
    lsb-release \
    ca-certificates \
    python3.12-venv \
    python3.12-dev \
    python3-pip \
    && apt-get clean

# Add the deadsnakes PPA (for newer Python versions)
RUN add-apt-repository ppa:deadsnakes/ppa && apt-get update

# Install Python 3.12
RUN apt-get install -y python3.12

# Install MongoDB tools using MongoDB's official repository for Ubuntu 22.04 (Jammy)
RUN curl -fsSL https://www.mongodb.org/static/pgp/server-6.0.asc | tee /etc/apt/trusted.gpg.d/mongodb.asc
RUN echo "deb [arch=amd64] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list
RUN apt-get update && apt-get install -y mongodb-database-tools

# Set working directory
WORKDIR /app

# Copy everything from the current directory (local) to /app in the container
COPY . /app/

# Copy requirements.txt (optional, if it's already included by COPY .)
#COPY requirements.txt /app/

# Create a virtual environment and activate it
RUN python3.12 -m venv /app/venv

# Install dependencies from requirements.txt using the virtual environment
RUN /app/venv/bin/pip install --upgrade pip
RUN /app/venv/bin/pip install -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Command to run FastAPI using Uvicorn
CMD ["/app/venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
