# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Copy requirements.txt first (layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project files
COPY . .

# Expose port 5000
EXPOSE 5000

# Run Flask development server
CMD ["flask", "run", "--host=0.0.0.0"]
