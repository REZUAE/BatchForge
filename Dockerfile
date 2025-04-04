# Base Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy app files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the FastAPI port
EXPOSE 8000

# Start the API with Uvicorn
CMD ["uvicorn", "batchforge.api:app", "--host", "0.0.0.0", "--port", "8000"]
    