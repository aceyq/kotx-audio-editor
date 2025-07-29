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
    try:
        # Get values from form
        start_raw = request.form.get("start", "0")
        end_raw = request.form.get("end", "0")
        fade_in_raw = request.form.get("fade_in", "2000")
        fade_out_raw = request.form.get("fade_out", "2000")

        app.logger.info(f"Received form data: start={start_raw}, end={end_raw}, fade_in={fade_in_raw}, fade_out={fade_out_raw}")

        # Convert to numbers
        start = float(start_raw) * 1000
        end = float(end_raw) * 1000
        fade_in = int(fade_in_raw)
        fade_out = int(fade_out_raw)

        # Check for valid values
        if end <= start:
            return "Error: End time must be after start time", 400

        input_path = session.get("audio_path")  # Check if you're saving it in session
        if not input_path:
            return "Error: No audio loaded", 400

        output_path = "static/final.mp3"

        # Process audio
        edit_audio(input_path, start, end, fade_in, fade_out, output_path)

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        app.logger.error(f"Error in /process: {e}", exc_info=True)
        return f"Internal Server Error: {e}", 500