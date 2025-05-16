# Use an official light Python image as the base image 
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the whole project into the container
COPY requirements.txt .
COPY . .

# Install any necessary Python packages
RUN pip install -r requirements.txt && rm -rf /root/.cache/pip

# fastapi, gradio default port
EXPOSE 8000 7860

# run based on docker-compose.yml
CMD ["echo", "Build success"]