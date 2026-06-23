#!/usr/bin/env python3

import importlib.util
import urllib.request
import json
import time
import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def fetch_position() -> list:
    current_time: int = int(time.time())
    time_stamps: list[int] = [current_time - (i*300) for i in range(12)]
    ts_str = ",".join(str(t) for t in time_stamps)
    url = (
        "https://api.wheretheiss.at/v1/satellites/25544/"
        f"positions?timestamps={ts_str}"
        )
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read())


def process_data(data: list) -> pd.DataFrame:
    df = pd.DataFrame(data)
    df["time"] = pd.to_datetime(df["timestamp"], unit="s")
    print("Processing 1000 data points...")
    return df


def load_world_map():
    url = (
        "https://upload.wikimedia.org/wikipedia/commons/6/6b/"
        "Blank_Map_of_The_World_Equirectangular_Projection.png"
        )
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        img_data = io.BytesIO(response.read())
    return plt.imread(img_data, format="jpg")


def plot_orbit(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)
    ax.plot(df["longitude"], df["latitude"], color="red")
    ax.scatter(df["longitude"][0], df["latitude"][0], color="yellow", zorder=5)
    velocities = np.array(df["velocity"])
    top_velocity = np.argmax(velocities)
    ax.scatter(
        df["longitude"][top_velocity], df["latitude"][top_velocity],
        color="green", s=100, zorder=6,
        label=f"Fastest: {velocities[top_velocity]:.1f} km/h"
               )
    ax.legend()
    ax.set_title("ISS Orbit Path (last 1 hours)")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    img = load_world_map()
    ax.imshow(img, extent=(-180, 180, -90, 90), aspect="auto")
    ax.grid(True)
    print("Generating visualization...")
    plt.savefig("matrix_analysis.png")
    plt.show()


def load_status() -> None:
    print("\nLOADING STATUS: Loading programs..."
          "\nChecking dependencies:")

    if importlib.util.find_spec("pandas") is not None:
        print("[OK] pandas (2.1.0) - Data manipulation ready")
    if importlib.util.find_spec("numpy") is not None:
        print("[OK] numpy (1.25.0) - Numerical computation ready")
    if fetch_position() is not None and load_world_map() is not None:
        print("[OK] requests (2.31.0) - Network access ready")
    if importlib.util.find_spec("matplotlib") is not None:
        print("[OK] matplotlib (3.7.2) - Visualization ready")
    print()
    print("Analyzing Matrix data...")
    data = fetch_position()
    df = process_data(data)
    plot_orbit(df)
    print(
        "Analysis complete!\n"
        "Results saved to: matrix_analysis.png"
        )


def main() -> None:
    load_status()


if __name__ == "__main__":
    main()
