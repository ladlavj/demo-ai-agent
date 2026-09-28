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

# Expose Streamlit's default port
EXPOSE 8501

# Healthcheck to verify Streamlit is running
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# By default, start the Streamlit Web UI. 
# (You can override this by passing 'python -m src.main' to the docker run command)
CMD ["streamlit", "run", "src/chat_ui.py", "--server.port=8501", "--server.address=0.0.0.0"]
