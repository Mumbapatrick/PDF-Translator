from flask import Flask, request, send_file, jsonify, render_template_string
from flask_cors import CORS
from pdf_translate import translate_pdf_text_only  # ✅ Ensure this function exists
import os
import uuid

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Define upload and output folders
UPLOAD_FOLDER = "uploads"
TRANSLATED_FOLDER = os.path.expanduser("~/Downloads/translated")

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TRANSLATED_FOLDER, exist_ok=True)

# ---------------------- COMMON LANGUAGES ----------------------
# Predefined language options for dropdown (label | code)
COMMON_LANGUAGES = {
    "English": "en",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Chinese (Simplified)": "zh-CN",
    "Japanese": "ja",
    "Russian": "ru",
    "Portuguese": "pt",
    "Italian": "it",
    "Arabic": "ar"
}

# ---------------------- ROUTES ----------------------

@app.route("/")
def index():
    """Render the HTML upload interface with fixed language options"""
    language_options = "".join(
        [f'<option value="{code}">{name}</option>' for name, code in COMMON_LANGUAGES.items()]
    )

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🌍 PDF Translator</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f7f9fb;
                color: #333;
                padding: 40px;
            }}
            .container {{
                background: white;
                border-radius: 10px;
                padding: 25px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                max-width: 480px;
                margin: auto;
            }}
            h2 {{
                text-align: center;
                color: #007bff;
            }}
            label {{
                font-weight: bold;
                display: block;
                margin-top: 15px;
            }}
            input, select, button {{
                width: 100%;
                padding: 10px;
                margin-top: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                box-sizing: border-box;
            }}
            button {{
                background: #007bff;
                color: white;
                border: none;
                cursor: pointer;
                font-weight: bold;
                transition: background 0.3s;
            }}
            button:hover {{
                background: #0056b3;
            }}
            footer {{
                margin-top: 25px;
                font-size: 13px;
                color: #777;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🌍 PDF Translator Widget</h2>
            <form action="/translate" method="post" enctype="multipart/form-data">
                <label for="file">Upload a PDF:</label>
                <input type="file" name="file" accept=".pdf" required>

                <label for="language">Select Target Language:</label>
                <select name="language" required>
                    {language_options}
                </select>

                <button type="submit">Translate PDF</button>
            </form>
            <footer>Powered by Flask + Deep Translator</footer>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)


@app.route("/translate", methods=["POST"])
def handle_translate_pdf():
    """Handle uploaded file and perform translation"""
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    target_lang = request.form.get("language", "en")

    if not file.filename:
        return jsonify({"error": "Empty filename"}), 400

    # Save uploaded file
    input_pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_pdf_path)

    # Define translated file path
    output_pdf_name = f"{uuid.uuid4()}_{file.filename}"
    output_pdf_path = os.path.join(TRANSLATED_FOLDER, output_pdf_name)

    # Try translating
    try:
        translate_pdf_text_only(input_pdf_path, output_pdf_path, target_lang)
    except Exception as e:
        return jsonify({"error": f"Translation failed: {str(e)}"}), 500

    # Return translated file
    return send_file(
        output_pdf_path,
        as_attachment=True,
        download_name=f"translated_{file.filename}",
        mimetype="application/pdf"
    )


# ---------------------- MAIN ENTRY ----------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
