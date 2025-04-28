FROM python:3.11-slim

WORKDIR /app

# Set environment variables 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 


RUN pip install --upgrade pip 

# Copy requirements early for Docker layer caching
COPY requirements.txt /app/

# Install system dependencies for OpenCV, Pillow, etc.
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies 
RUN pip install --no-cache-dir -r requirements.txt

# Add the full application code
ADD . /app/

# Expose the app port
EXPOSE 8000


# Run Django’s development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
