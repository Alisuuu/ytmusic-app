from flask import Flask, request, jsonify, render_template, send_file
from ytmusicapi import YTMusic
import yt_dlp
import os

app = Flask(__name__)
ytmusic = YTMusic()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    query = request.args.get("q")
    results = ytmusic.search(query, filter="songs")
    return jsonify(results)

@app.route("/stream")
def stream():
    video_id = request.args.get("id")
    url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        'format': 'bestaudio',
        'quiet': True,
        'noplaylist': True,
        'skip_download': True,
        'forceurl': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info['url']

    return jsonify({'audio_url': audio_url})

@app.route("/download")
def download():
    video_id = request.args.get("id")
    url = f"https://www.youtube.com/watch?v={video_id}"
    filename = f"downloads/{video_id}.mp3"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': filename,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
    
