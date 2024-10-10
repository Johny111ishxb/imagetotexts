from flask import Flask, request, jsonify, render_template
import requests
import firebase_admin
from firebase_admin import credentials, storage
import os

app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")  # Your service account key
firebase_admin.initialize_app(cred, {
    'storageBucket': 'imagetotext-4c3e3.appspot.com'  # Replace with your Firebase bucket
})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Check file format
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return jsonify({"error": "File format not supported. Please upload a PNG or JPG file."}), 400

    # Upload file to Firebase Storage
    bucket = storage.bucket()
    blob = bucket.blob(file.filename)
    try:
        blob.upload_from_file(file, content_type=file.content_type)

        # Get the file URL
        file_url = blob.public_url

        # Call the OCR.Space API
        ocr_url = "https://api.ocr.space/parse/image"
        api_key = "your_ocr_space_api_key"  # Replace with your OCR.Space API key
        payload = {'apikey': api_key, 'language': 'eng', 'url': file_url}
        response = requests.post(ocr_url, data=payload)
        result = response.json()

        if result.get("ParsedResults"):
            return jsonify({"text": result["ParsedResults"][0]["ParsedText"]})
        else:
            return jsonify({"error": result.get("ErrorMessage", "OCR failed")}), 500

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))  # Use the port from the environment variable
    app.run(host='0.0.0.0', port=port)
