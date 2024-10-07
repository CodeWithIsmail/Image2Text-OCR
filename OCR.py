from flask import Flask

app = Flask(__name__)

@app.route('/extract-text', methods=['GET'])
@app.route('/extract-img', methods=['GET'])
def extract_text_api():
    return "<h1>Hello ocr</h1"

def extract_text_api():
    return "<h1>Hello img</h1"

if __name__ == "__main__":
    app.run()
