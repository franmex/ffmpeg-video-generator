from flask import Flask, request, send_file
import subprocess
import requests
import librosa
import os

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_video():
    try:
        data = request.json
        image_urls = data.get("images", [])
        audio_url = data.get("audio", "")

        if not image_urls or not audio_url:
            return {"error": "Faltan imágenes o audio"}, 400

        # Descargar imágenes
        for i, url in enumerate(image_urls):
            response = requests.get(url)
            if response.status_code != 200:
                return {"error": f"Error al descargar imagen {i}"}, 500
            with open(f"image_{i}.jpg", "wb") as f:
                f.write(response.content)

        # Descargar audio
        response = requests.get(audio_url)
        if response.status_code != 200:
            return {"error": "Error al descargar el audio"}, 500
        with open("audio.wav", "wb") as f:
            f.write(response.content)

        # Calcular duración del audio
        audio_duration = librosa.get_duration(filename="audio.wav")
        num_images = len(image_urls)
        time_per_image = audio_duration / num_images if num_images > 0 else 0

        # Generar video con FFmpeg
        subprocess.run([
            "ffmpeg", "-y",
            "-framerate", f"1/{time_per_image}",
            "-i", "image_%d.jpg",
            "-i", "audio.wav",
            "-c:v", "libx264",
            "-vf", "fps=25,format=yuv420p",
            "-shortest",
            "output.mp4"
        ], check=True)

        return send_file("output.mp4", mimetype="video/mp4")

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
