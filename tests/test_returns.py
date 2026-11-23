from pathlib import Path

import pytest

from engine.deal import load_deal
from engine.returns import moic
from engine.waterfall import run_waterfall

DEMO = Path(__file__).parent.parent / "demos" / "reference_deal.json"
EQUITY_INVESTED = 35_000_000  # $350,000 in cents


def equity_received(scenario: str) -> int:
    """Total the equity investors got back in one scenario of the reference deal."""
    deal = load_deal(DEMO)
    paid = run_waterfall(deal["scenarios"][scenario], deal["tiers"])
    return paid["Equity recoupment"] + paid["Investor profit share"]


def test_moic_matches_excel_in_all_three_scenarios():
    assert moic(equity_received("flop"), EQUITY_INVESTED) == pytest.approx(0.3371, abs=0.0001)
    assert moic(equity_received("base"), EQUITY_INVESTED) == pytest.approx(2.0886, abs=0.0001)
    assert moic(equity_received("breakout"), EQUITY_INVESTED) == pytest.approx(5.0886, abs=0.0001)


def test_moic_with_nothing_invested_raises_an_error():
    with pytest.raises(ValueError):
        moic(100, 0)