# Use the official Python 3.10 slim image for a smaller footprint
FROM python:3.10-slim

# Prevent Python from writing .pyc files to disk and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (if any are needed by MCP servers or pip packages)
# RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Set path to avoid issues with Streamlit finding the correct working directory
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Expose Streamlit's default port
EXPOSE 8501

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Use the entrypoint script to dynamically start the chosen interface(s)
ENTRYPOINT ["./entrypoint.sh"]
