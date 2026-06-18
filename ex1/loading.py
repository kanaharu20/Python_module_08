#!/usr/bin/env python3

import urllib.request
import urllib.parse
import json
import time
# import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def fetch_position() -> list:
    current_time: int = int(time.time())
    time_stamps: list[int] = [current_time - (i*300) for i in range(36)]
    ts_str = ",".join(str(t) for t in time_stamps)
    url = f"https://api.wheretheiss.at/v1/satellites/25544/positions?timestamps={ts_str}"
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read())


def process_data(data: list) -> pd.DataFrame:
    df = pd.DataFrame(data)
    df["time"] = pd.to_datetime(df["timestamp"], unit="s")
    return df


def plot_orbit(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)
    ax.plot(df["longitude"], df["latitude"])
    ax.scatter(df["longitude"][0], df["latitude"][0], color="red", zorder=5)
    ax.set_title("ISS Orbit Path (last 3 hours)")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.grid(True)
    plt.show()


def main() -> None:
    data = fetch_position()
    df = process_data(data)
    plot_orbit(df)
    print(df)


main()
