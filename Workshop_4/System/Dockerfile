# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including R
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    r-base \
    r-base-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install R packages
RUN R -e "install.packages(c('caret', 'randomForest', 'xgboost', 'jsonlite', 'data.table'), repos='https://cloud.r-project.org/')"

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p OUT/models

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run the API
CMD ["python", "Presentation Layer/api.py"]
