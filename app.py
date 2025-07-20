from flask import Flask, render_template, send_file
import qrcode
import socket
import os
from pathlib import Path
from threading import Lock

app = Flask(__name__)
VISITOR_FILE = Path("visitors.txt")
lock = Lock()

def get_public_url():
    # For deployment you can set PUBLIC_URL env var,
    # otherwise auto‑detect LAN IP for local test.
    env = os.getenv("PUBLIC_URL")
    if env:
        return env.rstrip("/") + "/start"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return f"http://{local_ip}:5000/start"
    except:
        return "http://127.0.0.1:5000/start"

def increment_visitor():
    with lock:
        VISITOR_FILE.touch(exist_ok=True)
        count = int(VISITOR_FILE.read_text() or "0") + 1
        VISITOR_FILE.write_text(str(count))
        return count

@app.route('/')
def qr_page():
    link = get_public_url()
    # generate QR code
    img = qrcode.make(link)
    img.save("static/qr_code.png")
    # read current visitors (without increment)
    VISITOR_FILE.touch(exist_ok=True)
    visitors = int(VISITOR_FILE.read_text() or "0")
    return render_template("qr_page.html",
                           shop_name="Radhika Bar & Restro Tumasr Dewhadi",
                           qr_image="qr_code.png",
                           link=link,
                           visitors=visitors)

@app.route('/start')
def stopwatch():
    # increment on each actual game‐start visit
    visitors = increment_visitor()
    return render_template("stopwatch.html",
                           shop_name="Radhika Bar and Restaurant",
                           visitors=visitors)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
