def pay_tier(cash: int, owed: int) -> tuple[int, int]:
    """Pay off as of 'owed' as 'cash' allows. Returns (paid, cash_left)."""
    paid = min(cash, owed)
    return paid, cash - paid

def amount_owed(tier: dict, gross: int, cash: int) -> int:
    """How much a tier is due, in cents."""
    kind = tier["kind"]
    if kind == "percent_of_gross":
        return round(gross * tier["value"])
    if kind == "fixed":
        return tier["value"]
    if kind == "share_of_remaining":
        return round(cash * tier["value"])
    raise ValueError(f"Unknown tier kind: {kind}")


def run_waterfall(gross: int, tiers: list[dict]) -> dict[str, int]:
    """Pay gross revenue (in cents) through the tiers, in order.

    Returns how much each tier was paid, keyed by tier name.
    """
    cash = gross
    paid_by_tier = {}
    for tier in tiers:
        owed = amount_owed(tier, gross, cash)
        paid, cash = pay_tier(cash, owed)
        paid_by_tier[tier["name"]] = paid
    return paid_by_tier
