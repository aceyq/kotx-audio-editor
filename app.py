from flask import Flask, render_template, request, send_file
import os
from downloader import download_audio
from editor import edit_audio

app = Flask(__name__)

# Make sure "downloads" directory exists
if not os.path.exists("downloads"):
    os.makedirs("downloads")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        youtube_url = request.form.get("youtube_url")
        if not youtube_url:
            return render_template("index.html", error="Please enter a YouTube URL")

        try:
            # Download audio and return filename + path
            filename, mp3_path = download_audio(youtube_url)
            return render_template("waveform.html", mp3_file=mp3_path, filename=filename)
        except Exception as e:
            print("Download Error:", e)
            return render_template("index.html", error=f"Download failed: {e}")

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

        input_path = os.path.join("downloads", filename)
        output_path = os.path.join("downloads", "final.mp3")

        # Cut audio and add countdown (editor.py should handle countdown logic)
        edit_audio(input_path, start, end, fade_in, fade_out, output_path)

        # Send processed file back for download
        return send_file(output_path, as_attachment=True)

    except Exception as e:
        print("ERROR in /process:", e)
        return f"Error processing audio: {e}", 500


if __name__ == "__main__":
    app.run(debug=True)
