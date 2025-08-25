# app.py
import time

from flask import Flask, jsonify
from flask_cors import CORS

from gpiozero.pins.lgpio import LGPIOFactory
from gpiozero import LED

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

def activate_pin(pin_num):
    try:
        pin = LED(pin_num)
        pin.off()
        time.sleep(2)
        pin.on()
    except Exception as e:
        print(f"Erro ao acionar saída {pin_num}: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
