from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from editor import edit_audio
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Save uploaded MP3 file
        file = request.files['mp3_file']
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        # Redirect to waveform editor page
        return redirect(url_for("waveform", filename=filename))
    
    return render_template("index.html")

@app.route("/waveform/<filename>")
def waveform(filename):
    return render_template("waveform.html", mp3_file=url_for('uploaded_file', filename=filename))

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

@app.route("/process", methods=["POST"])
def process_audio():
    start = int(float(request.form["start"]) * 1000)
    end = int(float(request.form["end"]) * 1000)
    fade_in = int(request.form.get("fade_in", 0))
    fade_out = int(request.form.get("fade_out", 0))
    input_file = request.form["filename"]

    input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_file)
    output_path = os.path.join(PROCESSED_FOLDER, "final.mp3")

    edit_audio(input_path, start, end, fade_in, fade_out, output_path)

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)