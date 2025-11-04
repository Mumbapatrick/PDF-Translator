🗒️ Project Notes — 🌍 MultiLanguage PDF Translator

Overview:
A Python Flask-based web application that translates PDF files into multiple languages.
Supports text-based PDFs (and can later be extended for OCR-based scanned PDFs).
Users upload a PDF, choose a target language, and receive a translated version maintaining layout and structure.

✅ Key Features

Upload and translate PDFs via a simple web interface.

Supports 100+ languages through Google Translator.

Automatically populates the supported languages list in the dropdown.

Clean, minimal, and responsive user interface.

Preserves text formatting and layout for readability.

Handles multi-page and large documents efficiently.

Lightweight design — fast and easy to deploy.

Cross-platform compatible (desktop & mobile browsers).

🌍 Supported Languages

All languages supported by Google Translator API.

Language options load dynamically during app initialization.

⚙️ System Requirements

Python Version: 3.10+

Libraries (defined in requirements.txt):

Flask
Flask-Cors
deep-translator
reportlab
PyPDF2


Optional tools for future OCR:

pytesseract
Pillow

🧰 Installation & Setup

Clone or upload the project:

git clone https://github.com/Mumbapatrick/PDF-Translator.git 
cd pdf_translator


Install required libraries:

pip install -r requirements.txt


Run the application:

python app.py


Access the web interface:

http://127.0.0.1:5000

☁️ Deployment Notes (for Abyss or any platform)

Ensure your root folder includes:

app.py
pdf_translate.py
requirements.txt
uploads/


Start command:

python app.py


Port: 5000 (exposed to the web server)

The platform will automatically install all dependencies listed in requirements.txt.

🧩 Project Files

run.py → Main Flask application entry point.

pdf_translate.py → Contains translation and PDF handling logic.

uploads/ → Stores uploaded PDF files.

translated/ → Saves processed and translated files.

requirements.txt → Lists required dependencies.

💡 Future Enhancements

Add OCR support for scanned/image PDFs using Tesseract.

Allow batch translation of multiple PDFs.

Enable saving translation history per user.

Integrate cloud services (Google Drive, Dropbox).

Add authentication for personalized usage.

👤 Author

Mumba Patrick
ICT Professional | Developer | Cybersecurity Advocate
🌐 Focused on building accessible, multilingual, tech-driven communication tools.
