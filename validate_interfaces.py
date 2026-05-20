import csv
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def normalize_enabled(value):
    return value.strip().lower() in {"true", "yes", "1", "up", "enabled"}


def main():
    inventory = json.loads((BASE_DIR / "inventory.json").read_text(encoding="utf-8"))["devices"]
    rows = list(csv.DictReader((BASE_DIR / "interfaces.csv").open("r", encoding="utf-8", newline="")))
    failures = []

    for row in rows:
        device_name = row["device"].strip()
        interface_name = row["interface"].strip()
        config_path = BASE_DIR / inventory[device_name]["config_file"]

        if not config_path.exists():
            failures.append(f"{device_name}: missing simulated config file")
            continue

        config = json.loads(config_path.read_text(encoding="utf-8"))
        actual = config.get("interfaces", {}).get(interface_name)
        expected = {
            "description": row["description"].strip(),
            "ip_address": row["ip_address"].strip(),
            "subnet_mask": row["subnet_mask"].strip(),
            "enabled": normalize_enabled(row["enabled"]),
        }

        if actual != expected:
            failures.append(f"{device_name} {interface_name}: expected {expected}, got {actual}")

    if failures:
        print("Validation failed:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print("Validation passed. Simulated devices match interfaces.csv.")


if __name__ == "__main__":
    main()
