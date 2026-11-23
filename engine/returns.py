from engine.waterfall import run_waterfall


def moic(received: int, invested: int) -> float:
    """Multiple on invested capital: total received divided by total invested.

    1.0 means the investor got exactly their money back; 2.0 means double.
    """
    if invested <= 0:
        raise ValueError("Invested amount must be more than zero")
    return received / invested


def npv(rate: float, cash_flows: list[float]) -> float:
    """Net present value: each year's cash flow discounted back to today.

    cash_flows[0] is today (year 0), cash_flows[1] is one year from now, and so on.
    """
    return sum(cf / (1 + rate) ** year for year, cf in enumerate(cash_flows))


def irr(cash_flows: list[float], low: float = -0.99, high: float = 10.0) -> float:
    """Internal rate of return, found by bisection.

    Searches between `low` (-99%) and `high` (1000%) for the rate where NPV is zero.
    """
    if (npv(low, cash_flows) > 0) == (npv(high, cash_flows) > 0):
        raise ValueError("No IRR found between -99% and 1000% for these cash flows")
    for _ in range(100):
        mid = (low + high) / 2
        if npv(mid, cash_flows) > 0:
            low = mid   # still positive: the true rate is higher
        else:
            high = mid  # negative: the true rate is lower
    return (low + high) / 2

def received_by(gross: int, tiers: list, names: list[str]) -> int:
    """Total paid to the named tiers or parties at a given gross revenue (cents)."""
    paid = run_waterfall(gross, tiers)
    return sum(paid.get(name, 0) for name in names)


def breakeven_gross(tiers: list, names: list[str], invested: int,
                    max_gross: int = 10**12) -> int:
    """Smallest gross revenue (in cents) at which `names` together get back `invested`.

    Uses binary search over whole cents, from $0 up to `max_gross` ($10 billion).
    """
    if received_by(max_gross, tiers, names) < invested:
        raise ValueError("These parties never break even, even at very high revenue")
    low, high = 0, max_gross
    while low < high:
        mid = (low + high) // 2
        if received_by(mid, tiers, names) >= invested:
            high = mid      # enough: breakeven is here or lower
        else:
            low = mid + 1   # not enough: breakeven is higher
    return low