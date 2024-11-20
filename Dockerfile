# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy application code to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 4000 in the container
EXPOSE 4000

# Command to run the Flask app
CMD ["python", "main.py"]
