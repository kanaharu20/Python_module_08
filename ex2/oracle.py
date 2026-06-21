#!/usr/bin/env python3

import os
from dotenv import load_dotenv


def main() -> None:
    print("\nORACLE STATUS: Reading the Matrix...\n")

    load_dotenv()
    print("Configuration loaded:")
    matrix_mode: str = os.getenv("MATRIX_MODE")
    database_url: str = os.getenv("DATABASE_URL")
    api_kry: str = os.getenv("API_KEY")
    log_level: str = os.getenv("LOG_LEVEL")
    zion_endpoint: str = os.getenv("ZION_ENDPOINT")
    print(f"Mode: {matrix_mode}")
    print(f"Database: {database_url}")
    print(f"API Access: {api_kry}")
    print(f"Log Level: {log_level}")
    print(f"Zion Network: {zion_endpoint}")
    print()
    print("Environment security check:")


    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    main()


