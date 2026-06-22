#!/usr/bin/env python3

import sys
import os
import site


def main() -> None:
    print("\nMATRIX STATUS: ", end="")
    in_venv: bool = False
    if sys.base_prefix == sys.prefix:
        print("You're still plugged in\n")
    else:
        print("Welcome to the construct\n")
        in_venv = True
    if not in_venv:
        print(f"Current Python: {os.path.realpath(sys.executable)}")
        print("Virtual Environment: ", end="")
        print(" None detected\n")
        print(
            "WARNING: You're in the global environment!\n"
            "The machines can see everything you install.\n"
            )
        print(
            "To enter the construct, run:\n"
            "python -m venv matrix_env\n"
            "source matrix_env/bin/activate # On Unix\n"
            "matrix_env\\Scripts\\activate # On Windows\n")
        print("Then run this program again.")
    else:
        print(f"Current Python: {sys.executable}")
        print("Virtual Environment: ", end="")
        venv_name = os.path.basename(sys.prefix)
        print(venv_name)
        print(f"Environment Path: {sys.prefix}\n")
        print(
            "SUCCESS: You're in an isolated environment!\n"
            "Safe to install packages without affecting\n"
            "the global system.\n"
            )
        print(
            "Package installation path: \n"
            f"{site.getusersitepackages()}"
            )


if __name__ == "__main__":
    main()
