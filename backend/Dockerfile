# Use a slim Python base image
FROM python:3.9-slim

WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application with Uvicorn
# This allows the server to be accessible from other containers
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
