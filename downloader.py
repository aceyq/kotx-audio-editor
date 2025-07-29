import yt_dlp   # Python tool that can download YouTube videos/audio
import uuid   # to create unique IDs

def download_audio(youtube_url):
    # unique filename without extension first
    base_name = f"song_{uuid.uuid4().hex}"
    output_file = f"{base_name}.mp3"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': base_name + ".%(ext)s",  # let yt-dlp decide extension
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }
        ]
    }

    # download the file from YouTube
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])  # needs 2 tabs!

    return output_file

#ydl is a dictionary
#format picks the best quality audio available
#outtmpl: tells what file name to save it as 
#postprocessors: after downloading, use a tool called FFmpeg to extract audio/save it as mp3
#FFmpeg: a BTS tool yt_dlp uses to convert videos to audio formats, no need to install separately, because yt_dlp handles it
#yt_dlp.YoutubeDL(ydl_opts) -> creates a "downloader object" with our options
#with __ as ydl: -> with keyword makes sure the downloader runs and cleans up properly
#ydl.download([youtube_url]) -> downloads the Youtube link