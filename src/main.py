import json
import os
import socket
import time
from datetime import UTC, datetime

config_path = "data/config.json"
history_path = "data/history.json"
template_path = "site/template.html"
output_dir = "site"
output_html = "site/index.html"


def load_json_file(file_path, default_factory=list):
    if not os.path.exists(file_path):
        return default_factory()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default_factory()


def check_target_availability(host, port, timeout=2.0):
    start_time = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True, round((time.perf_counter() - start_time) * 1000, 2)
    except OSError:
        return False, 0.0


def calculate_uptime(target_history):
    if not target_history:
        return 0.0
    online_count = sum(1 for check in target_history if check.get("is_online"))
    return round((online_count / len(target_history)) * 100, 2)


def main():
    targets = load_json_file(config_path, list)
    if not targets:
        print("File does not exist.")

    history = load_json_file(history_path, dict)
    now_utc = datetime.now(UTC).isoformat()
    table_rows = ""

    for target in targets:
        host = target.get("host")
        port = target.get("port")
        name = target.get("name", "Unknown Target")

        if not host or not port:
            continue

        is_online, latency = check_target_availability(
            host, port, target.get("timeout", 2.0)
        )

        target_key = f"{host}:{port}"
        if target_key not in history:
            history[target_key] = []

        history[target_key].append(
            {"timestamp": now_utc, "is_online": is_online, "latency_ms": latency}
        )

        uptime = calculate_uptime(history[target_key])

        print(
            f"[{'ONLINE' if is_online else 'OFFLINE'}] {name} ({target_key}) "
            f"- {latency} ms / Uptime: {uptime}%"
        )

        status_class = "online" if is_online else "offline"
        status_text = "Online" if is_online else "Offline"

        table_rows += f"""
        <tr>
            <td><strong>{name}</strong></td>
            <td><code>{target_key}</code></td>
            <td><span class="status-badge {status_class}">{status_text}</span></td>
            <td>{latency} ms</td>
            <td>{uptime}%</td>
        </tr>
    """

    os.makedirs(os.path.dirname(history_path), exist_ok=True)
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()

        rendered_html = template.replace("{last_updated}", now_utc).replace(
            "{table_rows}", table_rows
        )

        os.makedirs(output_dir, exist_ok=True)
        with open(output_html, "w", encoding="utf-8") as f:
            f.write(rendered_html)


if __name__ == "__main__":
    main()
