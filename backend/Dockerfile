# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install flask flask-cors


# Copy the rest of the application code into the container at /app
COPY . .

# Create ui directory (will be mounted at runtime)
RUN mkdir -p /app/ui

# Expose the port the app runs on
EXPOSE 5000

# Define the command to run your app using Flask
CMD ["python", "impo.py"]
