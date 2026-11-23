from hypothesis import given, settings
from hypothesis import strategies as st

from engine.waterfall import run_waterfall

# Building blocks for random deals.
money = st.integers(min_value=0, max_value=10**10)          # $0 to $100 million, in cents
rate = st.floats(min_value=0, max_value=1, allow_nan=False)  # 0% to 100%
multiple = st.floats(min_value=1, max_value=3, allow_nan=False)  # 1x to 3x payback

TIER_KINDS = ["percent_of_gross", "fixed", "share_of_remaining", "recoup", "pari_passu"]


@st.composite
def random_tier(draw, i):
    """Invent one random tier of any kind."""
    kind = draw(st.sampled_from(TIER_KINDS))
    name = f"Tier {i}"
    if kind in ("percent_of_gross", "share_of_remaining"):
        return {"name": name, "kind": kind, "value": draw(rate)}
    if kind == "fixed":
        return {"name": name, "kind": kind, "value": draw(money)}
    if kind == "recoup":
        return {"name": name, "kind": kind,
                "principal": draw(money), "multiple": draw(multiple)}
    party_count = draw(st.integers(min_value=1, max_value=4))
    parties = [{"name": f"{name} party {j}",
                "principal": draw(money), "multiple": draw(multiple)}
               for j in range(party_count)]
    return {"name": name, "kind": kind, "parties": parties}


@st.composite
def random_deal(draw):
    """Invent a whole deal: 0 to 8 random tiers, plus a final tier that takes what's left."""
    tier_count = draw(st.integers(min_value=0, max_value=8))
    tiers = [draw(random_tier(i)) for i in range(tier_count)]
    tiers.append({"name": "Residual", "kind": "share_of_remaining", "value": 1.0})
    return tiers


@settings(max_examples=1000)
@given(gross=money, tiers=random_deal())
def test_money_is_never_created_or_lost(gross, tiers):
    paid = run_waterfall(gross, tiers)
    assert all(amount >= 0 for amount in paid.values())
    assert sum(paid.values()) == gross