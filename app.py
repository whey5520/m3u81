from flask import Flask, render_template, request, jsonify, send_file
import subprocess
import os

app = Flask(__name__)

def download_and_convert_video(input_url, output_file='output.mp4'):
    command = [
        'ffmpeg',
        '-y',
        '-i', input_url,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', 'experimental',
        output_file
    ]
    try:
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=300)
        if process.returncode == 0:
            print(f"FFmpeg success: saved {output_file}")
            return True, output_file
        else:
            print("FFmpeg error:", process.stderr)
            return False, process.stderr
    except Exception as e:
        print("Exception running FFmpeg:", e)
        return False, str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    data = request.get_json()
    url = data.get('url', '').strip()
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    if url.endswith('.m3u8') or url.endswith('.mp4'):
        return jsonify({'direct_link': url})

    output_file = 'output.mp4'

    if os.path.exists(output_file):
        os.remove(output_file)

    success, result = download_and_convert_video(url, output_file)
    if success:
        return jsonify({'message': 'Video processed and saved on server.', 'download_url': '/download'})
    else:
        return jsonify({'error': 'Failed to process video.', 'details': result}), 500

@app.route('/download')
def download():
    output_file = 'output.mp4'
    if os.path.exists(output_file):
        return send_file(output_file, as_attachment=True)
    else:
        return "File not found. Please process a video first.", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
