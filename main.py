import os
import firebase_admin
from firebase_admin import credentials, storage
from flask import Flask, request, jsonify, render_template

# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'imagetotext-4c3e3.appspot.com'  # Replace with your Firebase project ID
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

    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return jsonify({"error": "File format not supported. Please upload a PNG or JPG file."}), 400

    try:
        # Upload image to Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(f"uploads/{file.filename}")
        blob.upload_from_file(file, content_type=file.content_type)

        # Get the public URL of the uploaded image
        blob.make_public()
        image_url = blob.public_url

        # Use image_url to send to OCR API
        # ... (Add your OCR code here)

        return jsonify({"message": "File uploaded successfully", "image_url": image_url})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))  # Get port from environment variable
    app.run(host='0.0.0.0', port=port)

