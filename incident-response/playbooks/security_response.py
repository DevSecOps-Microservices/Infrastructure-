from datetime import datetime, timezone

def handle_security_alert(alert):
    labels = alert.get("labels", {})
    annotations = alert.get("annotations", {})
    alertname = labels.get("alertname", "unknown")
    application = labels.get("application", labels.get("job", "unknown"))
    summary = annotations.get("summary", "")
    severity = labels.get("severity", "unknown")

    print(
        f"[SECURITY] alert={alertname} target={application} severity={severity} "
        f"detected_at={datetime.now(timezone.utc).isoformat()} summary=\"{summary}\"",
        flush=True,
    )
    print(f"[SECURITY] no auto-block available — logged for manual review", flush=True)