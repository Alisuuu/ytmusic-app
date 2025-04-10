from flask import Flask, request, jsonify, send_from_directory
from ytmusicapi import YTMusic
import yt_dlp
import os

app = Flask(__name__, static_folder='static', static_url_path='')
ytmusic = YTMusic()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/search')
def search():
    query = request.args.get('q')
    results = ytmusic.search(query, filter='songs')
    return jsonify(results)

@app.route('/download')
def download():
    video_id = request.args.get('id')
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'downloads/{video_id}.%(ext)s',
        'quiet': True,
        'noplaylist': True,
    }
    os.makedirs("downloads", exist_ok=True)
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filepath = info['requested_downloads'][0]['filepath']
        filename = os.path.basename(filepath)
    return jsonify({'filename': filename, 'url': f'/file/{filename}'})

@app.route('/file/<filename>')
def serve_file(filename):
    return send_from_directory('downloads', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
