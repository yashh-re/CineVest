import json
from pathlib import Path

PRESETS_FILE = Path(__file__).parent.parent / "presets" / "incentives.json"


def load_presets(path: str | Path = PRESETS_FILE) -> dict:
    """Read the state incentive presets."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def incentive_amount(state: str, qualifying_spend: int, rate: float | None = None,
                     presets: dict | None = None) -> dict[str, int]:
    """Work out a production's tax credit for one state.

    `qualifying_spend` is in cents. `rate` defaults to the state's base rate.
    Returns the credit's face value and its cash value after any broker discount.
    """
    presets = presets or load_presets()
    if state not in presets["states"]:
        raise ValueError(f"No incentive preset for '{state}'")
    preset = presets["states"][state]

    if rate is None:
        rate = preset["base_rate"]
    if not preset["base_rate"] <= rate <= preset["max_rate"]:
        raise ValueError(
            f"{preset['name']} rate must be between "
            f"{preset['base_rate']:.0%} and {preset['max_rate']:.0%}"
        )

    credit = round(qualifying_spend * rate)
    if preset["per_project_cap"] is not None:
        credit = min(credit, preset["per_project_cap"])
    cash_value = round(credit * (1 - preset["broker_discount"]))
    return {"credit": credit, "cash_value": cash_value}