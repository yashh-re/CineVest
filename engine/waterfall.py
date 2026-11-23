from engine.models import Tier


def pay_tier(cash: int, owed: int) -> tuple[int, int]:
    """Pay as much of `owed` as `cash` allows. Returns (paid, cash_left)."""
    paid = min(cash, owed)
    return paid, cash - paid


def party_owed(party) -> int:
    """What a Party (or a recoup Tier) is due: principal times multiple, in cents."""
    return round(party.principal * party.multiple)


def split_pro_rata(amount: int, weights: list[int]) -> list[int]:
    """Split `amount` in proportion to `weights`.

    Every share but the last is rounded down; the last share takes whatever
    is left, so the shares always add up to exactly `amount`.
    """
    total = sum(weights)
    if total == 0:
        return [0] * len(weights)
    shares = [amount * w // total for w in weights[:-1]]
    shares.append(amount - sum(shares))
    return shares


def amount_owed(tier: Tier, gross: int, cash: int) -> int:
    """How much a tier is due, in cents."""
    if tier.kind == "percent_of_gross":
        return round(gross * tier.value)
    if tier.kind == "fixed":
        return tier.value
    if tier.kind == "share_of_remaining":
        return round(cash * tier.value)
    if tier.kind == "recoup":
        return party_owed(tier)
    if tier.kind == "pari_passu":
        return sum(party_owed(p) for p in tier.parties)
    raise ValueError(f"Unknown tier kind: {tier.kind}")


def run_waterfall(gross: int, tiers: list) -> dict[str, int]:
    """Pay gross revenue (in cents) through the tiers, in order.

    `tiers` can be Tier objects or plain dictionaries (as loaded from JSON).
    Returns how much each tier (or each pari passu party) was paid, by name.
    """
    tiers = [t if isinstance(t, Tier) else Tier.from_dict(t) for t in tiers]
    cash = gross
    paid_by_tier = {}
    for tier in tiers:
        owed = amount_owed(tier, gross, cash)
        paid, cash = pay_tier(cash, owed)
        if tier.kind == "pari_passu":
            weights = [party_owed(p) for p in tier.parties]
            for party, share in zip(tier.parties, split_pro_rata(paid, weights)):
                paid_by_tier[party.name] = share
        else:
            paid_by_tier[tier.name] = paid
    return paid_by_tier