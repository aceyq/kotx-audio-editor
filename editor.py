from pydub import AudioSegment #library for editing audio
#this class lets you slice, fade, and export 
from pydub.utils import which

# Force pydub to use ffmpeg explicitly
AudioSegment.converter = which("ffmpeg")


def edit_audio(input_file, start_ms, end_ms, fade_in_ms = 0, fade_out_ms = 0, output_file="edited.mp3"):
    #optional fade lengths, default is 0
    song = AudioSegment.from_mp3(input_file)
    #loads the MP3 into memory as an AudioSegment object 
    cut = song[start_ms:end_ms]
    #trims audio by slicing like a list (e.g. song[10000:30000] is 10s-30s)

    if fade_in_ms:
        cut = cut.fade_in(fade_in_ms)
    if fade_out_ms:
        cut = cut.fade_out(fade_out_ms)

    # Load countdown audio
    countdown = AudioSegment.from_mp3("countdown.mp3")

    # Combine countdown + cut audio
    final = countdown + cut  # '+' concatenates in pydub

    final.export(output_file, format = 'mp3')
    return output_file


