from flask import Flask, request
import subprocess, json

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot ready - compliant upload version"

@app.route('/upload', methods=['POST'])
def upload():
    request.files['map'].save("map.jpg")
    request.files['audio'].save("audio.mp3")
    with open("meta.json", "w") as f:
        f.write(request.files['meta'].read().decode())

    cmd = ["ffmpeg", "-y", "-loop", "1", "-i", "map.jpg", "-i", "audio.mp3", "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac", "-shortest", "-pix_fmt", "yuv420p", "video.mp4"]
    subprocess.run(cmd)
    return "Video created - now upload via YouTube API", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
