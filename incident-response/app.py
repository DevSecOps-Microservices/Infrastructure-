from flask import Flask, request, jsonify
from playbooks.service_down import restart_service

app = Flask(__name__)


@app.route("/")
def home():
    return "Incident Response Service"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    print("[WEBHOOK] Alert received", flush=True)

    for alert in data.get("alerts", []):
        status = alert.get("status")
        labels = alert.get("labels", {})

        alert_name = labels.get("alertname")
        service = labels.get("service")

        print(
            f"[WEBHOOK] alert={alert_name}, "
            f"status={status}, service={service}",
            flush=True
        )

        if status == "firing" and alert_name == "ServiceDown":
            if service:
                print(
                    f"[PLAYBOOK] Executing service-down playbook "
                    f"for {service}",
                    flush=True
                )

                restart_service(service)

            else:
                print(
                    "[PLAYBOOK] No service specified in alert",
                    flush=True
                )

    return jsonify({"status": "processed"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)