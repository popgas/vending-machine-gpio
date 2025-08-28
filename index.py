# app.py
import base64
import time

from flask import Flask, jsonify
from flask_cors import CORS

import lgpio
from gpiozero.pins.lgpio import LGPIOFactory
from gpiozero import LED
import cv2

factory = LGPIOFactory(chip=0)

app = Flask(__name__)

CORS(app)

@app.get("/trigger/<pin>")
def home(pin):
    activate_pin(pin)
    return jsonify(status="ok")
@app.get("/health")
def health():
    return jsonify(status="ok")

@app.get("/available-cameras")
def list_cameras(max_tested=10):
    available_cameras = []
    for i in range(max_tested):
        cap = cv2.VideoCapture(i)
        if cap is not None and cap.isOpened():
            available_cameras.append(i)
            cap.release()

    return jsonify(available_cameras=available_cameras)

@app.get("/take-photo/<camera>")
def take_photo(camera):
    cap = cv2.VideoCapture(int(camera))

    try:
        if not cap.isOpened():
            raise ValueError("Não foi possível abrir a câmera")

        time.sleep(1)
        ret, frame = cap.read()

        if not ret or frame is None:
            raise ValueError("Não foi possível abrir a câmera")

        success, buffer = cv2.imencode('.jpg', frame)

        if not success:
            raise RuntimeError("Falha ao codificar o frame em JPEG")

        jpg_bytes = buffer.tobytes()
        b64_str = base64.b64encode(jpg_bytes).decode('utf-8')

        # Monta o Data URI
        base64_image = f"data:image/jpeg;base64,{b64_str}"

        return jsonify(status="ok", image=base64_image)
    except Exception as e:
        raise

    finally:
        cap.release()

def activate_pin(pin_num):
    try:
        pin = LED(pin_num)
        pin.off()
        time.sleep(2)
        pin.on()
    except Exception as e:
        print(f"Erro ao acionar saída {pin_num}: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
