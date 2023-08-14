# Use the official Python image as the base image
FROM python:3.8

# Copy the current directory into the container at /app
COPY . /app

# Set the working directory to /app
WORKDIR /app

# Install any needed dependencies specified in requirements.txt
RUN apt-get update && apt-get install -y python && pip install -r requirements.txt

# Expose the port that the app runs on
EXPOSE $PORT

# Define the command to run your app using Gunicorn
CMD ["gunicorn", "--workers=4", "--bind", "0.0.0.0:$PORT", "app:app"]
