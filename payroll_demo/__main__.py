"""Run with: python -m payroll_demo build"""

import argparse
from pathlib import Path

from .pipeline import export_snapshot


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a synthetic payroll migration snapshot")
    parser.add_argument("command", choices=["build"])
    args = parser.parse_args()
    if args.command == "build":
        destination = Path(__file__).resolve().parents[1] / "site" / "data" / "snapshot.json"
        print(f"Snapshot sintético: {export_snapshot(destination)}")


if __name__ == "__main__":
    main()
