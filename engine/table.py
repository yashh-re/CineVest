import math

from engine.models import Tier

COLUMNS = ["Name", "Kind", "Rate (%)", "Amount ($)", "Principal ($)", "Multiple"]
RATE_KINDS = ("percent_of_gross", "share_of_remaining")


def _is_blank(value) -> bool:
    """True for None, empty text, or pandas' 'not a number' empty cell."""
    if value is None:
        return True
    if isinstance(value, float) and math.isnan(value):
        return True
    return isinstance(value, str) and not value.strip()


def _number(row: dict, column: str) -> float:
    """Read a number from a row, or explain which cell is missing."""
    value = row.get(column)
    if _is_blank(value):
        raise ValueError(f"Tier '{row['Name']}': please fill in '{column}'")
    return float(value)


def _cents(row: dict, column: str) -> int:
    """Read a dollar amount from a row and convert it to cents."""
    return round(_number(row, column) * 100)


def rows_to_tiers(rows: list[dict]) -> list[Tier]:
    """Turn on-screen table rows (dollars, percentages) into engine Tiers (cents, fractions)."""
    tiers = []
    seen_names = set()
    for row in rows:
        if _is_blank(row.get("Name")):
            continue  # skip empty rows
        name = str(row["Name"]).strip()
        if name in seen_names:
            raise ValueError(f"Two tiers are both called '{name}'. Please rename one.")
        seen_names.add(name)

        kind = row.get("Kind")
        tier = {"name": name, "kind": kind}
        if kind in RATE_KINDS:
            tier["value"] = _number(row, "Rate (%)") / 100
        elif kind == "fixed":
            tier["value"] = _cents(row, "Amount ($)")
        elif kind == "recoup":
            tier["principal"] = _cents(row, "Principal ($)")
            tier["multiple"] = _number(row, "Multiple")
        tiers.append(Tier.from_dict(tier))
    return tiers


def tiers_to_rows(tiers: list) -> list[dict]:
    """Turn engine tiers into table rows, for showing a saved deal on screen."""
    rows = []
    for tier in tiers:
        tier = tier if isinstance(tier, Tier) else Tier.from_dict(tier)
        row = dict.fromkeys(COLUMNS)  # every column, all empty
        row["Name"] = tier.name
        row["Kind"] = tier.kind
        if tier.kind in RATE_KINDS:
            row["Rate (%)"] = round(tier.value * 100, 6)
        elif tier.kind == "fixed":
            row["Amount ($)"] = tier.value / 100
        elif tier.kind == "recoup":
            row["Principal ($)"] = tier.principal / 100
            row["Multiple"] = tier.multiple
        else:
            raise ValueError(f"Tier '{tier.name}': {tier.kind} tiers can't be shown in the table yet")
        rows.append(row)
    return rows