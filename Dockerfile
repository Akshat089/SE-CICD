# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app

# Copy application files
COPY todo.py /app/
COPY tests/ /app/tests/

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Create a non-root user for security
RUN useradd -m -u 1000 todouser && \
    chown -R todouser:todouser /app

# Switch to non-root user
USER todouser

# Set the default command to run the application
CMD ["python", "todo.py"]
