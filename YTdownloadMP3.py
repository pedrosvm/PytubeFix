
from pytubefix import YouTube
from pytubefix.cli import on_progress
import re
import os
import subprocess

url = input('Insira a URL do vídeo Baixar MP3: ')

yt = YouTube(url, on_progress_callback=on_progress, use_po_token=True)
print(yt.title)

# Título seguro para nome de arquivo
safe_title = re.sub(r'[\\/*?:"<>|]', "", yt.title)

# Pega só o áudio
ys = yt.streams.get_audio_only()

# Define nome temporário do arquivo baixado
download_path = ys.download(filename="temp_audio")
output_path = f"{safe_title}.mp3"

# Converte pra MP3 com ffmpeg
subprocess.run([
    "ffmpeg", "-i", download_path,
    "-vn", "-ab", "192k", "-ar", "44100", "-y",
    output_path
])

# Remove o arquivo temporário
os.remove(download_path)

print(f"Download finalizado: {output_path}")


