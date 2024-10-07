import os
import cv2
import pytesseract
from flask import Flask, request, jsonify

app = Flask(__name__)

# Specify the path to the Tesseract executable (optional, if it's not in PATH)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    text = pytesseract.image_to_string(gray)
    return text

@app.route('/extract-text', methods=['POST'])
def extract_text_api():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    
    # Save the uploaded image temporarily
    temp_image_path = os.path.join('uploads', image_file.filename)
    image_file.save(temp_image_path)

    try:
        extracted_text = extract_text(temp_image_path)
        return jsonify({"extracted_text": extracted_text})
    finally:
        # Remove the temporary file
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
