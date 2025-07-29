from flask import Flask, render_template, request, send_file, send_from_directory
import os
from werkzeug.utils import secure_filename
from editor import edit_audio

UPLOAD_FOLDER = "uploads"
app = Flask(__name__)

# Ensure uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if not file or file.filename == "":
            return render_template("index.html", error="Please upload a valid MP3")

        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Pass a PUBLIC URL to waveform.html
        mp3_url = f"/uploads/{filename}"
        return render_template("waveform.html", mp3_file=mp3_url, filename=filename)

    return render_template("index.html")


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


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