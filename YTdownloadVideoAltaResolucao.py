from pytubefix import YouTube
from pytubefix.cli import on_progress

url = input("Insira a URL do vídeo: ")
yt = YouTube(url, on_progress_callback=on_progress, use_po_token=True)

print(f"\nTítulo do vídeo: {yt.title}")
print("\nStreams de vídeo disponíveis:\n")

video_streams = yt.streams.filter(adaptive=True, only_video=True).order_by('resolution').desc()
for i, stream in enumerate(video_streams, 1):
    print(f"{i}. Resolução: {stream.resolution}, FPS: {stream.fps}, MIME: {stream.mime_type}, Codec: {stream.video_codec}, itag: {stream.itag}")

# Exibe opções e deixa o usuário escolher
choice = int(input("\nDigite o número da stream que deseja baixar: ")) - 1
video_stream = video_streams[choice]

# Baixa o áudio normalmente
audio_stream = yt.streams.filter(adaptive=True, only_audio=True, file_extension='mp4').order_by('abr').desc().first()

# Define nomes
video_file = "temp_video." + video_stream.subtype
audio_file = "temp_audio.mp4"
output_file = yt.title.replace(" ", "_").replace("/", "_") + ".mp4"

print(f"\nBaixando vídeo: {video_stream.resolution} ({video_stream.mime_type})")
video_stream.download(filename=video_file)

print("Baixando áudio...")
audio_stream.download(filename=audio_file)

# Junta com ffmpeg
import subprocess, os
subprocess.run([
    "ffmpeg", "-y",
    "-i", video_file,
    "-i", audio_file,
    "-c:v", "copy",
    "-c:a", "aac",
    output_file
])

os.remove(video_file)
os.remove(audio_file)

print(f"\nDownload finalizado: {output_file}")
