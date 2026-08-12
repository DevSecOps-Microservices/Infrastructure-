from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    alert_data = request.get_json()

    print("=== ALERTMANAGER ALERT RECEIVED ===")
    print(alert_data)

    return jsonify({"status": "received"}), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "UP"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)