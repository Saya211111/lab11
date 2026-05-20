import csv
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
INVENTORY_PATH = BASE_DIR / "inventory.json"
SOURCE_OF_TRUTH_PATH = BASE_DIR / "interfaces.csv"


def load_inventory():
    with INVENTORY_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)["devices"]


def load_source_of_truth():
    with SOURCE_OF_TRUTH_PATH.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def load_device_config(path):
    if not path.exists():
        return {"hostname": path.stem, "interfaces": {}}

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_device_config(path, config):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(config, file, indent=2, sort_keys=True)
        file.write("\n")


def normalize_enabled(value):
    return value.strip().lower() in {"true", "yes", "1", "up", "enabled"}


def deploy():
    inventory = load_inventory()
    rows = load_source_of_truth()
    changes = []

    for row in rows:
        device_name = row["device"].strip()
        interface_name = row["interface"].strip()

        if device_name not in inventory:
            raise ValueError(f"{device_name} exists in interfaces.csv but not inventory.json")

        config_path = BASE_DIR / inventory[device_name]["config_file"]
        config = load_device_config(config_path)
        config["hostname"] = device_name

        desired = {
            "description": row["description"].strip(),
            "ip_address": row["ip_address"].strip(),
            "subnet_mask": row["subnet_mask"].strip(),
            "enabled": normalize_enabled(row["enabled"]),
        }

        current = config["interfaces"].get(interface_name)
        if current != desired:
            config["interfaces"][interface_name] = desired
            changes.append(f"{device_name} {interface_name}")

        save_device_config(config_path, config)

    if changes:
        print("Updated simulated interfaces:")
        for item in changes:
            print(f"- {item}")
    else:
        print("No changes needed. Simulated devices already match interfaces.csv.")


if __name__ == "__main__":
    deploy()
