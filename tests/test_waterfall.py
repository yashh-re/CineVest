import pytest

from engine.waterfall import pay_tier, run_waterfall


def usd(dollars):
    """Convert whole dollars to cents, so tests read like the spreadsheet."""
    return dollars * 100


def test_pays_in_full_when_cash_is_enough():
    assert pay_tier(cash=100, owed=60) == (60, 40)


def test_pays_what_it_can_when_cash_is_short():
    assert pay_tier(cash=50, owed=60) == (50, 0)


def test_pays_nothing_when_nothing_is_owed():
    assert pay_tier(cash=100, owed=0) == (0, 100)


def reference_tiers():
    """The reference deal from demos/reference_deal.xlsx."""
    return [
        {"name": "CAM fee", "kind": "percent_of_gross", "value": 0.01},
        {"name": "Sales agent fee", "kind": "percent_of_gross", "value": 0.15},
        {"name": "Sales expenses", "kind": "fixed", "value": usd(50_000)},
        {"name": "Gap loan", "kind": "recoup",
         "principal": usd(150_000), "multiple": 1.12},
        {"name": "Equity recoupment", "kind": "recoup",
         "principal": usd(350_000), "multiple": 1.20},
        {"name": "Investor profit share", "kind": "share_of_remaining", "value": 0.5},
        {"name": "Producer profit share", "kind": "share_of_remaining", "value": 1.0},
    ]


def test_base_case_matches_excel():
    paid = run_waterfall(usd(1_500_000), reference_tiers())
    assert paid == {
        "CAM fee": usd(15_000),
        "Sales agent fee": usd(225_000),
        "Sales expenses": usd(50_000),
        "Gap loan": usd(168_000),
        "Equity recoupment": usd(420_000),
        "Investor profit share": usd(311_000),
        "Producer profit share": usd(311_000),
    }


def test_flop_runs_out_during_equity_recoupment():
    paid = run_waterfall(usd(400_000), reference_tiers())
    assert paid["Gap loan"] == usd(168_000)
    assert paid["Equity recoupment"] == usd(118_000)
    assert paid["Investor profit share"] == 0
    assert paid["Producer profit share"] == 0


def test_breakout_case_matches_excel():
    paid = run_waterfall(usd(4_000_000), reference_tiers())
    assert paid["Sales agent fee"] == usd(600_000)
    assert paid["Investor profit share"] == usd(1_361_000)
    assert paid["Producer profit share"] == usd(1_361_000)


def test_every_dollar_is_paid_out():
    for gross in [usd(400_000), usd(1_500_000), usd(4_000_000)]:
        paid = run_waterfall(gross, reference_tiers())
        assert sum(paid.values()) == gross


def test_recoup_tier_adds_interest_or_premium():
    gap_loan = {"name": "Gap loan", "kind": "recoup",
                "principal": usd(150_000), "multiple": 1.12}
    equity = {"name": "Equity", "kind": "recoup",
              "principal": usd(350_000), "multiple": 1.20}
    paid = run_waterfall(usd(1_000_000), [gap_loan, equity])
    assert paid["Gap loan"] == usd(168_000)
    assert paid["Equity"] == usd(420_000)


def test_unknown_tier_kind_raises_an_error():
    typo = {"name": "Oops", "kind": "fixd", "value": 100}
    with pytest.raises(ValueError):
        run_waterfall(usd(1_000), [typo])