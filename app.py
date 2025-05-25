from flask import Flask, request, render_template, jsonify
import requests
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    data = request.json
    target_url = data.get('url')
    if not target_url:
        return jsonify({'error': 'Missing URL'}), 400

    try:
        res = requests.get(target_url, timeout=10)
        content = res.text

        mp4_links = list(set(re.findall(r'https?://[^\\s"\'>]+\\.mp4[^"\'\\s>]*', content)))
        m3u8_links = list(set(re.findall(r'https?://[^\\s"\'>]+\\.m3u8[^"\'\\s>]*', content)))

        return jsonify({
            'mp4': mp4_links,
            'm3u8': m3u8_links
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
