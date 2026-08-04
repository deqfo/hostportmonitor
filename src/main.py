import json
import os
import socket
import time
from datetime import UTC, datetime

config_path = "data/config.json"
history_path = "data/history.json"
template_path = "src/template.html"
output_dir = "site"
output_html = "src/index.html"

with open(config_path, "r", encoding="utf-8") as f:
    targets = json.load(f)

history = {}
if os.path.exists(history_path):
    try:
        with open(history_path, "r", encoding="utf-8") as f:
            history = json.load(f)
    except json.JSONDecodeError:
        history = {}


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


now_utc = datetime.now(UTC).isoformat()
table_rows = ""

for target in targets:
    is_online, latency = check_target_availability(
        target["host"], target["port"], target.get("timeout", 2.0)
    )

    target_key = f"{target['host']}:{target['port']}"
    if target_key not in history:
        history[target_key] = []

    history[target_key].append(
        {"timestamp": now_utc, "is_online": is_online, "latency_ms": latency}
    )

    uptime = calculate_uptime(history[target_key])

    print(
        f"[{'ONLINE' if is_online else 'OFFLINE'}] {target['name']} ({target_key}) "
        f"- {latency} ms / Uptime: {uptime}%"
    )

    status_class = "online" if is_online else "offline"
    status_text = "Online" if is_online else "Offline"

    table_rows += f"""
        <tr>
            <td><strong>{target["name"]}</strong></td>
            <td><code>{target_key}</code></td>
            <td><span class="status-badge {status_class}">{status_text}</span></td>
            <td>{latency} ms</td>
            <td>{uptime}%</td>
        </tr>
    """

with open(history_path, "w", encoding="utf-8") as f:
    json.dump(history, f, indent=2, ensure_ascii=False)

with open(template_path, "r", encoding="utf-8") as f:
    template = f.read()

rendered_html = template.replace("{last_updated}", now_utc).replace(
    "{table_rows}", table_rows
)

os.makedirs(output_dir, exist_ok=True)
with open(output_html, "w", encoding="utf-8") as f:
    f.write(rendered_html)
