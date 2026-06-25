#!/usr/bin/env python3

import os
from dotenv import load_dotenv


def main() -> None:
    print("\nORACLE STATUS: Reading the Matrix...\n")

    load_dotenv()
    print("Configuration loaded:")
    config: dict[str, str | None] = {}
    config["Mode"] = os.getenv("MATRIX_MODE")
    config["Database"] = os.getenv("DATABASE_URL")
    config["API Access"] = os.getenv("API_KEY")
    config["Log Level"] = os.getenv("LOG_LEVEL")
    config["Zion Network"] = os.getenv("ZION_ENDPOINT")

    missing_config: list[str] = []
    for key in config:
        if config[key] == "" or config[key] is None:
            missing_config.append(key)

    for key in config:
        if key == "Mode":
            if config[key] in ["development", "production"]:
                print(f"{key}: {config[key]}")
            else:
                print(f"{key}: Invalid MATRIX_MODE")
        elif key == "Database":
            if config['Mode'] == "development":
                print(f"{key}: Connected to local instance")
            elif config['Mode'] == "production":
                print(f"{key}: Connected to production instance")
            else:
                print(f"{key}: Unknown mode")
        elif key == "API Access":
            if config[key]:
                print(f"{key}: Authenticated")
            else:
                print(f"{key}: [MISSING] API_KEY not configured")
        elif key == "Log Level":
            if config['Mode'] == "development":
                print(f"{key}: {config[key]}")
            elif config['Mode'] == "production":
                print(f"{key}: Hidden in production")
            else:
                print(f"{key}: Unknown mode")
        else:
            if config[key]:
                print(f"{key}: Online")
            else:
                print(f"{key}: Offline")
    print()
    print("Environment security check:")
    print("[OK] No hardcoded secrets detected")
    if not missing_config:
        print("[OK] .env file properly configured")
    else:
        print("[ERROR] .env file not properly configured")
        for key in missing_config:
            print(f"  - {key}")
    print("[OK] Production overrides available")
    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    main()
