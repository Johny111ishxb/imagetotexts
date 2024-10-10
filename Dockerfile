# Use the official Python image from the Docker Hub
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies in one step
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port your app runs on
EXPOSE 3000

# Command to run your application with reduced workers
CMD ["sh", "-c", "gunicorn -w 1 -b 0.0.0.0:${PORT:-3000} server:app"]
