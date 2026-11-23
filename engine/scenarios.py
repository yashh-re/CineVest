from engine.waterfall import run_waterfall


def compare_scenarios(tiers: list, scenarios: dict[str, int]) -> list[dict]:
    """Run the waterfall at several revenue levels.

    Returns one row per payee, in payment order, with one column per scenario.
    All amounts in cents.
    """
    results = {label: run_waterfall(gross, tiers) for label, gross in scenarios.items()}
    names = list(run_waterfall(0, tiers).keys())  # payees, in payment order
    return [
        {"Who": name, **{label: results[label][name] for label in scenarios}}
        for name in names
    ]