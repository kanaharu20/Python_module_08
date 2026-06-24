#!/usr/bin/env python3

import importlib
import importlib.util
import urllib.request
import json
import time
import io


def check_deps() -> dict:
    deps = {
        "numpy": "np",
        "pandas": "pd",
        "matplotlib": "matplotlib",
        "matplotlib.pyplot": "plt",
    }
    mods = {}
    for module_name, alias in deps.items():
        if importlib.util.find_spec(module_name) is None:
            raise ImportError(f"[MISSING] {module_name} - install required")
        mods[alias] = importlib.import_module(module_name)
    return mods


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


def process_data(data: list, pd) -> object:
    df = pd.DataFrame(data)
    df["time"] = pd.to_datetime(df["timestamp"], unit="s")
    print("Processing 12 data points...")
    return df


def load_world_map(plt) -> object:
    url = (
        "https://upload.wikimedia.org/wikipedia/commons/6/6b/"
        "Blank_Map_of_The_World_Equirectangular_Projection.png"
        )
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        img_data = io.BytesIO(response.read())
    return plt.imread(img_data, format="png")


def plot_orbit(df, mods: dict) -> None:
    np = mods["np"]
    plt = mods["plt"]
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)
    ax.plot(df["longitude"], df["latitude"], color="red")
    ax.scatter(
        df["longitude"].iloc[0], df["latitude"].iloc[0], color="yellow",
        zorder=5
        )
    velocities = np.array(df["velocity"])
    top_velocity = np.argmax(velocities)
    ax.scatter(
        df["longitude"].iloc[top_velocity], df["latitude"].iloc[top_velocity],
        color="green", s=100, zorder=6,
        label=f"Fastest: {velocities[top_velocity]:.1f} km/h"
               )
    ax.legend()
    ax.set_title("ISS Orbit Path (last 1 hours)")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    img = load_world_map(plt)
    ax.imshow(img, extent=(-180, 180, -90, 90), aspect="auto")
    ax.grid(True)
    print("Generating visualization...")
    plt.savefig("matrix_analysis.png")


def load_status() -> None:
    print("\nLOADING STATUS: Loading programs..."
          "\nChecking dependencies:")
    try:
        mods = check_deps()
        print(f"[OK] pandas ({mods['pd'].__version__}) "
              "- Data manipulation ready")
        print(f"[OK] numpy ({mods['np'].__version__}) "
              "- Numerical computation ready")
        if fetch_position() is not None:
            if load_world_map(mods["plt"]) is not None:
                print("[OK] requests - Network access ready")
        print(f"[OK] matplotlib ({mods['matplotlib'].__version__}) "
              "- Visualization ready")
        print()
        print("Analyzing Matrix data...")
        data = fetch_position()
        df = process_data(data, mods["pd"])
        plot_orbit(df, mods)
        print(
            "Analysis complete!\n"
            "Results saved to: matrix_analysis.png"
            )
    except ImportError as e:
        print(e)
        print_instraction()


def print_instraction() -> None:
    print()
    print("Missing dependencies detected.")
    print()
    print("Install with pip:")
    print("pip install -r requirements.txt")
    print()
    print("Or install with Poetry:")
    print("poetry install")


def pip_vs_poetry() -> None:
    print("=== pip vs Poetry ===")

    print("pip:")
    print("- Uses requirements.txt")
    print("- Installs dependencies with: pip install -r requirements.txt")
    print("- Usually manages only package installation")
    print("- Does not manage project metadata by itself")

    print()
    print("Poetry:")
    print("- Uses pyproject.toml")
    print("- Installs dependencies with: poetry install")
    print("- Manages project metadata and dependencies together")
    print("- Can create and manage virtual environments")


def main() -> None:
    load_status()
    print()
    pip_vs_poetry()


if __name__ == "__main__":
    main()
