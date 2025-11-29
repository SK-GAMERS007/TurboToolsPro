from pytube import YouTube
import os

def download_audio(url):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    file = stream.download(filename="audio.mp4")

    # Convert to mp3 128kbps default
    final = "audio.mp3"
    os.rename(file, final)
    return final
