import docker
import sys
import time


def restart_service(service_name):
    client = docker.from_env()

    print(f"[PLAYBOOK] Service down detected: {service_name}", flush=True)
    print(f"[PLAYBOOK] Restarting {service_name}...", flush=True)

    try:
        container = client.containers.get(service_name)

        print(
            f"[PLAYBOOK] Current status: {container.status}",
            flush=True
        )

        container.restart(timeout=10)

        # Give Docker a moment to update the state
        time.sleep(2)

        container.reload()

        if container.status == "running":
            print(
                f"[PLAYBOOK] SUCCESS: {service_name} restarted successfully",
                flush=True
            )
            return True

        print(
            f"[PLAYBOOK] FAILURE: {service_name} is still "
            f"{container.status}",
            flush=True
        )
        return False

    except docker.errors.NotFound:
        print(
            f"[PLAYBOOK] FAILURE: container '{service_name}' not found",
            flush=True
        )
        return False

    except Exception as e:
        print(
            f"[PLAYBOOK] FAILURE: {type(e).__name__}: {e}",
            flush=True
        )
        return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Usage: python service-down.py <container-name>",
            flush=True
        )
        sys.exit(1)

    success = restart_service(sys.argv[1])
    sys.exit(0 if success else 1)