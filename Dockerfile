# Use Python 3.11 base image
FROM python:3.11-slim

# Install Tesseract OCR and OpenCV dependencies
RUN apt-get update && \
    apt-get install -y tesseract-ocr libtesseract-dev libleptonica-dev \
    libgl1-mesa-glx && \  # Add this line to install OpenGL library
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application files
COPY . .

# Expose the port for Flask
EXPOSE 5000

# Start the Flask app
CMD ["python", "OCR.py"]
