from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    data = request.get_json()
    url = data.get('url', '').strip()
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    # Just check if URL ends with .m3u8 or .mp4 and return it
    if url.endswith('.m3u8') or url.endswith('.mp4'):
        return jsonify({'direct_link': url})

    # Otherwise, say unsupported URL
    return jsonify({'error': 'Only direct .m3u8 or .mp4 URLs are supported'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
