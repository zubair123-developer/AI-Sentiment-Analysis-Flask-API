
import os
import hmac
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Read API keys securely from the environment
API_KEYS = {
    f"Consumer {i}": os.getenv(f"API_KEY_{i}")
    for i in range(1, 4)
}

if not all(API_KEYS.values()):
    raise RuntimeError("Please configure all three API keys in .env")

if len(set(API_KEYS.values())) != 3:
    raise RuntimeError("API keys must be unique")


@app.route("/process", methods=["POST"])
def process_text():
    supplied_key = request.headers.get("X-API-Key", "")

    # Authenticate the API consumer
    consumer = None
    for name, valid_key in API_KEYS.items():
        if hmac.compare_digest(supplied_key, valid_key):
            consumer = name
            break

    if consumer is None:
        return jsonify({
            "error": "Invalid or missing API key"
        }), 401

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "JSON object required"
        }), 400

    text = data.get("text")

    if not isinstance(text, str) or not text.strip():
        return jsonify({
            "error": "Please provide a valid text string"
        }), 400

    return jsonify({
        "consumer": consumer,
        "original_text": text,
        "processed_text": text.upper()
    }), 200


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5002,
        debug=False,
        use_reloader=False
    )
