import os
import time
import base64
from urllib.parse import urlparse, parse_qs, unquote
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, static_folder='static', template_folder='templates')

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "")
ADMIN_API_KEY = os.environ.get("ADMIN_API_KEY", "change-me")
PLATOBOOST = "https://gateway.platoboost.com/a/8?id="

CAPTCHA_TOKEN_STORE = {}

def send_discord_webhook(link):
    if not DISCORD_WEBHOOK_URL:
        print("No Discord webhook set, skipping.")
        return
    payload = {"embeds": [{"title": "Security Check!", "description": f"Open: {link}", "color": 5763719}]}
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
    except Exception as e:
        print("Webhook error:", e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/delta', methods=['POST'])
def delta():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({"status": "error", "error": "Missing URL"}), 400
    parsed = urlparse(url)
    q = parse_qs(parsed.query)
    id = q.get('id', [None])[0]
    if not id:
        return jsonify({"status": "error", "error": "Missing ID"}), 400

    send_discord_webhook(f"{PLATOBOOST}{id}")
    return jsonify({"status": "need_captcha", "message": f"CAPTCHA required for ID {id}", "id": id})

@app.route('/solve-token', methods=['POST'])
def solve_token():
    api_key = request.headers.get("X-API-KEY", "")
    if api_key != ADMIN_API_KEY:
        return jsonify({"status": "error", "error": "Unauthorized"}), 401
    data = request.get_json()
    id = data.get('id')
    token = data.get('token')
    if not id or not token:
        return jsonify({"status": "error", "error": "Missing ID or token"}), 400
    CAPTCHA_TOKEN_STORE[id] = token
    return jsonify({"status": "ok", "message": f"Token stored for {id}"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
  
