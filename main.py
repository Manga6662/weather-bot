from flask import Flask, request
import subprocess, os, json

app = Flask(__name__)

@app.route('/')
def home():
    return "Weather Bot - Compliant Version - Ready"

@app.route('/upload', methods=['POST'])
def upload():
    try:
        request.files['map'].save("map.jpg")
        request.files['audio'].save("audio.mp3")
        with open("meta.json", "w") as f:
            f.write(request.files['meta'].read().decode())
        
        # create video (compliant short video)
        cmd = ["ffmpeg", "-y", "-loop", "1", "-i", "map.jpg", "-i", "audio.mp3", "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac", "-shortest", "-pix_fmt", "yuv420p", "video.mp4"]
        subprocess.run(cmd, check=False)
        
        # For now just save, YouTube API upload will be added later
        with open("meta.json") as mf:
            meta = json.load(mf)
        return f"Video generated: {meta['title']}", 200
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
