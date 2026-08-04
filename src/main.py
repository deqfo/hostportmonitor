import json
import os


def load_config(filepath: str) -> list[dict]:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Súbor {filepath} nebol nájdený.")

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


config_path = "data/config.json"
print(load_config(config_path))
