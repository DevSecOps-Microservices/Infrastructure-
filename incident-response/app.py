from flask import Flask, request, jsonify
from playbooks.service_down import restart_service
from playbooks.security_response import handle_security_alert

app = Flask(__name__)

SECURITY_ALERTS = {
    "PossibleDDoS",
    "PossibleSQLInjection",
    "Excessive401Responses",
    "Excessive403Responses",
    "AbnormalTrafficSpike",
}


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
        service = labels.get("application")

        print(
            f"[WEBHOOK] alert={alert_name}, "
            f"status={status}, service={service}",
            flush=True
        )

        if status != "firing":
            continue

        if alert_name == "ServiceDown":
            if service:
                print(f"[PLAYBOOK] Executing service-down playbook for {service}", flush=True)
                try:
                    restart_service(service)
                except Exception as e:
                    print(f"[PLAYBOOK] failed to restart {service}: {e}", flush=True)
            else:
                print("[PLAYBOOK] No service specified in alert", flush=True)

        elif alert_name in SECURITY_ALERTS:
            try:
                handle_security_alert(alert)
            except Exception as e:
                print(f"[PLAYBOOK] security handler failed for {alert_name}: {e}", flush=True)

    return jsonify({"status": "processed"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)