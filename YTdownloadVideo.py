from pytubefix import YouTube
from pytubefix.cli import on_progress

url = input('Insira a URL do vídeo Baixar Vídeo: ')

# Adicionando use_po_token=True para evitar erro de BotDetection
yt = YouTube(url, on_progress_callback=on_progress, use_po_token=True)

print(f"Título do vídeo: {yt.title}")

ys = yt.streams.get_highest_resolution()
ys.download()
