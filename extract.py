from flask import Flask

app = Flask(__name__)

from pytubefix import YouTube
from pytubefix.cli import on_progress

# Create Youtube Object.
yt = YouTube('https://www.youtube.com/watch?v=OxAZE1v_BLM&ab_channel=MitchellMcKee', 
             on_progress_callback=on_progress)


audio = yt.streams.filter(only_audio=True).first()
if audio:
    print('Downloading Audio...')
    try:
        audio.download(filename=f'{yt.title}audio.mp4')
    except():
        print()
else:
    pass

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"