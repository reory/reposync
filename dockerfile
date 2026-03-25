# 1. Use Python 3.13 as the base image
FROM python:3.13-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Install system dependencies for Reflex (Node.js and Unzip)
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application code
COPY . .

# 6. Initialize and build the Reflex app
RUN reflex init
RUN reflex export --frontend-only --no-zip

# 7. Expose the port Reflex uses
EXPOSE 8000
EXPOSE 3000

# 8. Start the application with explicit ports and production flags
CMD ["reflex", "run", "--env", "prod", "--backend-port", "8000", "--frontend-port", "3000"]