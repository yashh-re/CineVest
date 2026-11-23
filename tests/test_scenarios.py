from pathlib import Path

from engine.deal import load_deal
from engine.scenarios import compare_scenarios

DEMO = Path(__file__).parent.parent / "demos" / "reference_deal.json"


def usd(dollars):
    return dollars * 100


SCENARIOS = {"Flop": usd(400_000), "Base": usd(1_500_000), "Breakout": usd(4_000_000)}


def test_compare_scenarios_matches_excel():
    tiers = load_deal(DEMO)["tiers"]
    rows = compare_scenarios(tiers, SCENARIOS)
    equity = next(row for row in rows if row["Who"] == "Equity recoupment")
    assert equity == {
        "Who": "Equity recoupment",
        "Flop": usd(118_000),
        "Base": usd(420_000),
        "Breakout": usd(420_000),
    }


def test_compare_scenarios_keeps_payment_order():
    tiers = load_deal(DEMO)["tiers"]
    rows = compare_scenarios(tiers, SCENARIOS)
    assert [row["Who"] for row in rows][:2] == ["CAM fee", "Sales agent fee"]