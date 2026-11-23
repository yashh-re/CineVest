import json
from pathlib import Path


def load_deal(path: str | Path) -> dict:
    """Read a deal from a JSON file."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_deal(deal: dict, path: str | Path) -> None:
    """Write a deal to a JSON file, formatted so people can read it."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(deal, f, indent=2)