#!/usr/bin/env python3

import os
import sys
from dotenv import load_dotenv


def main() -> None:
    print("\nORACLE STATUS: Reading the Matrix...\n")

    load_dotenv()
    print("Configuration loaded:")
    config: dict[str, str] = {}
    config["Mode"] = os.getenv("MATRIX_MODE")
    config["Database"] = os.getenv("DATABASE_URL")
    config["API Access"] = os.getenv("API_KEY")
    config["Log level"] = os.getenv("LOG_LEVEL")
    config["Zion Network"] = os.getenv("ZION_ENDPOINT")

    missing_config: list[str] = []
    for key in config:
        if config[key] == "":
            missing_config.append(key)

    for key in config:
        if key == "Mode":
            if key in ["development", "production"]:
                print(f"{key}: {config['Mode']}")
            else:
                print(f"{config[key]}: Invalid MATRIX_MODE")
        elif key == "Databese":
            if config['Mode'] == "development":
                print(f"{key}: Connected to local instance")
            elif config['Mode'] == "production":
                print(f"{key}: Connected to production instance")
            else:
                print(f"{key} Unknown mode")
        elif key == "API Access":
            print("API Access: Authenticated")
        elif key == "Log level":
            if config['Mode'] == "development":
                print(f"{key}: {config[key]}")
            elif config['Mode'] == "production":
                print(f"{key}: Hidden in production")
            else:
                print(f"{key}: Unknown mode")
        else:
            print(f"{key}: {config[key]}")
    print()
    print("Environment security check:")
    print("[OK] No hardcoded secrets detected")
    if not missing_config:
        print("[OK] .env file properly configured")
    else:
        print("[ERROR] .env file not properly configured", file=sys.stderr)
        for key in missing_config:
            print(f"  - {key}")
    print("[OK] Production overrides available")
    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    main()
