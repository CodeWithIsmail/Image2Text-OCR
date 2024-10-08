from flask import Flask, request, jsonify
import cv2
import pytesseract
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

# Set the Tesseract command path if necessary
# Make sure this path is correct for your Render environment
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Adjust this path if needed

# Function to extract text from the image
def extract_text(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # Extract text using pytesseract
    text = pytesseract.image_to_string(gray)

    return text

# API route to accept image and return extracted text
@app.route('/extract-text', methods=['POST'])
def extract_text_api():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    # Get the image file from the request
    image_file = request.files['image']
    
    # Convert the image file to an OpenCV-compatible format
    img = Image.open(io.BytesIO(image_file.read()))
    img = np.array(img)

    # Extract text from the image
    extracted_text = extract_text(img)

    # Return the extracted text as a JSON response
    return jsonify({"extracted_text": extracted_text})

@app.route('/check-tesseract', methods=['GET'])
def check_tesseract():
    try:
        output = pytesseract.image_to_string(np.zeros((100, 100, 3), dtype=np.uint8))  # An empty image
        return jsonify({"tesseract_installed": True, "output": output})
    except Exception as e:
        return jsonify({"tesseract_installed": False, "error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
