from flask import Flask, request, jsonify
import cv2
import pytesseract
import numpy as np
import re

app = Flask(__name__)

# Predefined list of test names for easier extraction
TEST_NAMES = ["cbc", "rbc", "wbc", "platelets", "hemoglobin"]

def preprocess_image(image_data):
    # Decode image bytes and preprocess it
    img_array = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return gray

def extract_test_values(text):
    # Use regular expressions to find test names and their values
    test_data = {}
    for line in text.splitlines():
        for test in TEST_NAMES:
            match = re.search(rf"\b{test}\b\s*:\s*(\d+\.?\d*)", line, re.IGNORECASE)
            if match:
                test_data[test] = float(match.group(1))
    return test_data

@app.route('/extract-text', methods=['POST'])
def extract_text():
    if 'image' not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400
    
    image_file = request.files['image'].read()
    preprocessed_image = preprocess_image(image_file)

    # Extract text using Tesseract
    extracted_text = pytesseract.image_to_string(preprocessed_image)

    # Parse for specific test values
    test_data = extract_test_values(extracted_text)

    return jsonify(test_data)

if __name__ == "__main__":
    app.run(debug=True)
