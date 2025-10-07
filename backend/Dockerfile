# Use a slim Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code
COPY . .

# The EXPOSE instruction is good for documentation but doesn't affect the runtime.
# The cloud platform will handle port mapping.
EXPOSE 8000

# Command to run the application with Uvicorn
# This version uses the $PORT environment variable provided by the deployment platform.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT"]