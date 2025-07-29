from flask import Flask, request, send_file, render_template, url_for
from downloader import download_audio
from editor import edit_audio
import os

app = Flask(__name__)
temp_file = ""


@app.route("/", methods=["GET", "POST"])
def index():
    global temp_file

    if "download" in request.form:
        url = request.form["url"]
        temp_file = download_audio(url)
        audio_url = url_for('serve_audio', filename=temp_file)
        return render_template("waveform.html", audio_file=audio_url)

    if "process" in request.form:
        start = int(float(request.form["start"]) * 1000)
        end = int(float(request.form["end"]) * 1000)
        fade_in = int(request.form.get("fade_in", 0))
        fade_out = int(request.form.get("fade_out", 0))

        output_file = "final.mp3"
        edit_audio(temp_file, start, end, fade_in, fade_out, output_file)

        os.remove(temp_file)
        return send_file(output_file, as_attachment=True)

    return render_template("index.html")


@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_file(filename)


if __name__ == "__main__":
    app.run(debug=True)
