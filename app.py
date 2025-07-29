from flask import Flask, render_template, request, send_file, send_from_directory, redirect, url_for
import os
from werkzeug.utils import secure_filename
from editor import edit_audio

# Folders
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"

app = Flask(__name__)

# Ensure folders exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        if not file or file.filename == "":
            return render_template("index.html", error="Please upload a valid MP3 file")

        # Save file
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Pass the uploaded MP3 path and filename to the cutting screen (waveform.html)
        return render_template("waveform.html", mp3_file=file_path, filename=filename)

    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process_audio():
    try:
        start = float(request.form.get("start", 0))
        end = float(request.form.get("end", 0))
        fade_in = int(request.form.get("fade_in", 0))
        fade_out = int(request.form.get("fade_out", 0))
        filename = request.form.get("filename")

        if not filename:
            return "Error: Missing filename", 400

        input_path = os.path.join(UPLOAD_FOLDER, filename)
        output_path = os.path.join(UPLOAD_FOLDER, "final.mp3")

        # Edit the audio (your editor.py should handle countdown & fade)
        edit_audio(input_path, start, end, fade_in, fade_out, output_path)

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        print("ERROR in /process:", e)
        return f"Error processing audio: {e}", 500


if __name__ == "__main__":
    app.run(debug=True)