from flask import Flask, render_template, request, jsonify
import fitz  # PyMuPDF for PDF text extraction
import os

app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def index():
    """Render the HTML frontend"""
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    """Handle PDF upload and extract text"""
    if "pdf" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["pdf"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    # Extract text from PDF
    extracted_text = extract_text(file_path)

    return jsonify({"text": extracted_text})

def extract_text(pdf_path):
    """Extract text from a PDF file"""
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text("text") for page in doc])
    return text

if __name__ == "__main__":
    app.run(debug=True)
