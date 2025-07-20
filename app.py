import os
from flask import Flask, render_template, redirect, url_for, request, session
import qrcode
from datetime import datetime

app = Flask(__name__)
app.secret_key = "any-secret-key"

VISITOR_FILE = "data/visitors.txt"

# Ensure visitor file exists
os.makedirs("data", exist_ok=True)
if not os.path.exists(VISITOR_FILE):
    with open(VISITOR_FILE, "w") as f:
        f.write("0")

# Helper: Get visitor count
def get_visitor_count():
    with open(VISITOR_FILE, "r") as f:
        return int(f.read().strip())

# Helper: Increment and save visitor count
def increment_visitor_count():
    count = get_visitor_count() + 1
    with open(VISITOR_FILE, "w") as f:
        f.write(str(count))
    return count

# Get full public Render URL here (update with your actual domain)
def get_public_url():
    return "https://radhikabar.onrender.com/start"  # CHANGE THIS after deployment

@app.route('/')
def home():
    # Generate QR code once
    img = qrcode.make(get_public_url())
    img.save("static/qr_code.png")

    visitors = get_visitor_count()
    return render_template("qr_page.html", visitors=visitors)

@app.route('/start')
def start_game():
    user_agent = request.headers.get('User-Agent')
    if "Mobile" in user_agent and "Tablet" not in user_agent and "iPad" not in user_agent:
        if session.get("played") == "yes":
            return redirect(url_for("already_played"))
        else:
            session["played"] = "yes"

    increment_visitor_count()
    return render_template("stopwatch.html")

@app.route('/already-played')
def already_played():
    return "You have already played. Please scan the QR again to try."

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
