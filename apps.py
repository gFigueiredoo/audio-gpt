import youtube_dl

ydl_opts = {
    'format': 'bestvideo[height<=720]+bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s'
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=0b9B-F_oA_o&ab_channel=SharkTankBrasil'])
