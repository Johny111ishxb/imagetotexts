from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

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

    # Ensure the uploaded file is an image (optional but recommended)
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return jsonify({"error": "File format not supported. Please upload a PNG or JPG file."}), 400

    # Get the language from the form (default to English if not provided)
    language = request.form.get('language', 'eng')

    # Validate that the language is supported by OCR.Space
    supported_languages = ['eng', 'ara', 'chs', 'cht', 'urd', 'fil', 'kor', 'jpn', 'spa', 'fre', 'ger']
    if language not in supported_languages:
        return jsonify({"error": f"Language '{language}' is not supported."}), 400

    if file:
        try:
            # Determine the file extension and set file type accordingly
            file_ext = file.filename.split('.')[-1].lower()
            file_type = file_ext.upper() if file_ext != 'jpeg' else 'JPG'

            # Sending image to OCR.Space API
            ocr_url = "https://api.ocr.space/parse/image"
            api_key = "153e0e5d8088957"  # Replace with your API key
            payload = {
                'apikey': api_key,
                'language': language,
                'isOverlayRequired': False,
                'filetype': file_type
            }
            files = {'file': file.read()}  # File content is read in binary form

            response = requests.post(ocr_url, data=payload, files=files)
            result = response.json()

            # Print the entire response for debugging
            print(result)  # Debugging: check the full response

            # Checking the response from the OCR API
            if result.get("ParsedResults"):
                return jsonify({"text": result["ParsedResults"][0]["ParsedText"]})
            else:
                return jsonify({"error": result.get("ErrorMessage", "OCR failed")}), 500

        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
