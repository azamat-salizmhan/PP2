# json.py

import json
import os

def main():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "sample-data.json")

    with open(file_path, "r") as file:
        data = json.load(file)

    print("Interface Status")
    print("=" * 80)
    print(f"{'DN':<50} {'Description':<20} {'Speed':<8} {'MTU':<6}")
    print("-" * 80)

    for item in data["imdata"]:
        attributes = item["l1PhysIf"]["attributes"]

        dn = attributes.get("dn", "")
        descr = attributes.get("descr", "")
        speed = attributes.get("speed", "")
        mtu = attributes.get("mtu", "")

        print(f"{dn:<50} {descr:<20} {speed:<8} {mtu:<6}")

if __name__ == "__main__":
    main()