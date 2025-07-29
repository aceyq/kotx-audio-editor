from editor import edit_audio

# Cut the first 20 seconds and fade in/out 2 seconds
edit_audio("song.mp3", start_ms=0, end_ms=20000, fade_in_ms=2000, fade_out_ms=2000)

print("Editing complete!")