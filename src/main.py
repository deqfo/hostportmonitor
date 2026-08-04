import json
import socket
import time

config_path = "data/config.json"
with open(config_path, "r", encoding="utf-8") as f:
    targets = json.load(f)


def check_target_availability(host, port, timeout=2.0):
    start_time = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True, round((time.perf_counter() - start_time) * 1000, 2)
    except OSError:
        return False, 0.0


for target in targets:
    is_online, latency = check_target_availability(
        target["host"], target["port"], target.get("timeout", 2.0)
    )
    print(
        f"[{'ONLINE' if is_online else 'OFFLINE'}] {target['name']} ({target['host']}:{target['port']}) - {latency} ms"
    )
