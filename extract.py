from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)

from pytubefix import YouTube
from pytubefix.cli import on_progress

def download_audio(url):
    try:
        print('fetch: ' + url)
        yt = YouTube(url, on_progress_callback=on_progress)
        audio = yt.streams.filter(only_audio=True).first()
    except:
        print('Error fetching url')
    if audio:
        try:
            print('Return stream')
            print(audio)
            return audio
        except:
            print("Failed to download file")
    else:
        print('Stream does not exist')

@app.route('/extract')
def extract_yt_audio():
    vid = request.args.get('vid')
    base_url = "https://www.youtube.com/watch?v="
    fetch_url = base_url + vid
    try:
        stream = download_audio(fetch_url)
    except:
        print('Error fetching url')
    if stream:
        directory_name = 'output'
        try:
            os.mkdir(directory_name)
            print(f"Directory '{directory_name}' created successfully.")
        except FileExistsError:
            print(f"Directory '{directory_name}' already exists.")
        except PermissionError:
            print(f"Permission denied: Unable to create '{directory_name}'.")
        except Exception as e:
            print(f"An error occurred: {e}")

        try:
            filepath = f'./output/{stream.default_filename}'
            stream.download(filename=filepath)
            print('Created file')
        except:
            print("Failed to download file")
    else:
        pass
    print('Send file')
    return send_from_directory('output', stream.default_filename)

# ---------------------------------------
# --------- Use for Debugging -----------
# ---------------------------------------

# url = input("URL >")
# download_audio(url)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    app.run(debug=True)