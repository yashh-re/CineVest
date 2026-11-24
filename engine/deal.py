import json
from dataclasses import asdict
from pathlib import Path

from engine.models import Tier


def load_deal(path: str | Path) -> dict:
    """Read a deal from a JSON file."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_deal(deal: dict, path: str | Path) -> None:
    """Write a deal to a JSON file, formatted so people can read it."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(deal, f, indent=2)


def tier_to_dict(tier: Tier) -> dict:
    """A Tier as a plain dictionary, leaving out the fields it doesn't use."""
    return {key: value for key, value in asdict(tier).items() if value is not None}


def build_deal(title: str, tiers: list[Tier], scenarios: dict[str, int],
               stack: dict) -> dict:
    """Bundle everything on screen into one deal, ready to save."""
    return {
        "title": title,
        "scenarios": scenarios,
        "stack": stack,
        "tiers": [tier_to_dict(tier) for tier in tiers],
    }


def deal_to_json(deal: dict) -> str:
    """A deal as JSON text, for the download button."""
    return json.dumps(deal, indent=2)


def deal_from_json(text: str) -> dict:
    """Read and check a deal from JSON text, such as an uploaded file.

    Raises ValueError with a clear message if the file isn't a valid deal.
    """
    deal = json.loads(text)  # not JSON at all -> ValueError
    if not isinstance(deal, dict) or not isinstance(deal.get("tiers"), list):
        raise ValueError("This file isn't a CineVest deal: it has no list of tiers.")
    for tier in deal["tiers"]:
        Tier.from_dict(tier)  # a bad tier -> ValueError naming the problem
    return deal