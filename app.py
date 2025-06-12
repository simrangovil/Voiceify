from flask import Flask, request, send_file
from gtts import gTTS
import os
from PyPDF2 import PdfReader
import docx

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_text(file_path, ext):
    if ext == ".pdf":
        reader = PdfReader(file_path)
        return " ".join([page.extract_text() or "" for page in reader.pages])
    elif ext == ".docx":
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    ext = os.path.splitext(file.filename)[1].lower()
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    text = extract_text(path, ext)
    tts = gTTS(text)
    audio_path = os.path.join(UPLOAD_FOLDER, "output.mp3")
    tts.save(audio_path)

    return send_file(audio_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
