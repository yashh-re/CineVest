import math
from pathlib import Path

import pytest

from engine.deal import load_deal
from engine.models import Tier
from engine.table import rows_to_tiers, tiers_to_rows

DEMO = Path(__file__).parent.parent / "demos" / "reference_deal.json"


def test_reference_deal_survives_a_round_trip_through_the_table():
    tiers = load_deal(DEMO)["tiers"]
    rows = tiers_to_rows(tiers)
    assert rows_to_tiers(rows) == [Tier.from_dict(t) for t in tiers]


def test_blank_rows_are_skipped():
    rows = [
        {"Name": "Fee", "Kind": "percent_of_gross", "Rate (%)": 10},
        {"Name": "", "Kind": None},
    ]
    assert len(rows_to_tiers(rows)) == 1


def test_missing_amount_names_the_tier():
    rows = [{"Name": "Sales expenses", "Kind": "fixed", "Amount ($)": None}]
    with pytest.raises(ValueError, match="Sales expenses"):
        rows_to_tiers(rows)


def test_empty_cell_from_pandas_counts_as_missing():
    rows = [{"Name": "Sales expenses", "Kind": "fixed", "Amount ($)": math.nan}]
    with pytest.raises(ValueError, match="Amount"):
        rows_to_tiers(rows)


def test_two_tiers_with_the_same_name_are_rejected():
    rows = [
        {"Name": "Gap loan", "Kind": "fixed", "Amount ($)": 100},
        {"Name": "Gap loan", "Kind": "fixed", "Amount ($)": 200},
    ]
    with pytest.raises(ValueError, match="Gap loan"):
        rows_to_tiers(rows)