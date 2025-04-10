from flask import Flask, request, jsonify
from ytmusicapi import YTMusic

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
