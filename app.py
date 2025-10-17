from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

BOT_API_URL = os.getenv("BOT_API_URL") 
BOT_API_KEY = os.getenv("BOT_API_KEY")

if not BOT_API_URL or not BOT_API_KEY:
    raise RuntimeError("Missing BOT_API_URL or BOT_API_KEY in env vars.")

@app.route("/")
def index():
    return "🍰 Kissa Flask API is running!"

@app.route("/order", methods=["POST"])
def order():
    print("📦 Raw data:", request.data)
    print("📦 JSON parsed:", request.get_json(silent=True))
    data = request.get_json()
    print("📦 Received order:", data)

    headers = {"X-API-Key": BOT_API_KEY}
    try:
        res = requests.post(f"{BOT_API_URL}/send", json=data, headers=headers, timeout=10)
        return jsonify(res.json()), res.status_code
    except Exception as e:
        print("⚠️ Error sending to bot:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)), debug=False)
