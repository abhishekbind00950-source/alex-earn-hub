import os
import hmac
from flask import Flask, jsonify, request

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = os.getenv("ADMIN_ID", "")


@app.get("/")
def home():
    return jsonify({
        "app": "ALEX EARN HUB",
        "status": "success",
        "message": "Earning platform API is running!",
        "version": "1.0.0"
    })


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/api/info")
def info():
    return jsonify({
        "name": "ALEX EARN HUB",
        "features": [
            "Telegram Mini App",
            "Referral System",
            "Reward Tasks",
            "Wallet",
            "Withdrawal Requests",
            "Admin Panel"
        ]
    })


@app.post("/api/bot/webhook")
def bot_webhook():
    secret = os.getenv("WEBHOOK_SECRET", "")
    supplied = request.headers.get(
        "X-Telegram-Bot-Api-Secret-Token", ""
    )

    if not secret or not hmac.compare_digest(secret, supplied):
        return jsonify({"error": "Unauthorized"}), 401

    update = request.get_json(silent=True) or {}

    # Telegram updates will be processed in a later step.
    return jsonify({
        "received": True,
        "update_id": update.get("update_id")
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "10000"))
    )
