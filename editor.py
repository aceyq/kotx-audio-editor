from pydub import AudioSegment
from pydub.utils import which

# Use ffmpeg for audio operations
AudioSegment.converter = which("ffmpeg")

def edit_audio(input_file, start, end, fade_in_ms=0, fade_out_ms=0, output_file="edited.mp3"):
    # Convert seconds (from waveform) to milliseconds
    start_ms = int(float(start) * 1000)
    end_ms = int(float(end) * 1000)

    # Load the original audio
    song = AudioSegment.from_mp3(input_file)

    # Crop the audio
    cut = song[start_ms:end_ms]
    if len(cut) <= 0:
        print(f"[ERROR] Cropped audio is empty! Start: {start_ms}, End: {end_ms}, Original length: {len(song)}ms")
        raise ValueError("Empty cropped audio")

    # Apply fades if specified
    if fade_in_ms:
        cut = cut.fade_in(fade_in_ms)
    if fade_out_ms:
        cut = cut.fade_out(fade_out_ms)

    # Load countdown and combine
    countdown = AudioSegment.from_mp3("countdown.mp3")
    final = countdown + cut

    # Export final file
    final.export(output_file, format='mp3')
    return output_file