from pathlib import Path

import pytest

from charts import ROLE_COLOURS, payee_roles, scenario_bar_chart
from engine.deal import load_deal
from engine.scenarios import compare_scenarios

DEMO = Path(__file__).parent.parent / "demos" / "reference_deal.json"
SCENARIOS = {"Flop": 40_000_000, "Base": 150_000_000, "Breakout": 400_000_000}
EQUITY = ["Equity recoupment", "Investor profit share"]


def make_chart():
    tiers = load_deal(DEMO)["tiers"]
    rows = compare_scenarios(tiers, SCENARIOS)
    return rows, scenario_bar_chart(rows, list(SCENARIOS))


def test_chart_has_one_segment_per_payee_in_payment_order():
    rows, fig = make_chart()
    assert [trace.name for trace in fig.data] == [row["Who"] for row in rows]


def test_each_bar_adds_up_to_that_scenarios_revenue():
    rows, fig = make_chart()
    for i, (label, gross_cents) in enumerate(SCENARIOS.items()):
        bar_total = sum(trace.y[i] for trace in fig.data)
        assert bar_total == pytest.approx(gross_cents / 100)


def test_roles_follow_the_kind_of_tier():
    tiers = load_deal(DEMO)["tiers"]
    assert payee_roles(tiers, EQUITY) == {
        "CAM fee": "Fees & costs",
        "Sales agent fee": "Fees & costs",
        "Sales expenses": "Fees & costs",
        "Gap loan": "Lenders",
        "Equity recoupment": "Investors",
        "Investor profit share": "Investors",
        "Producer profit share": "Producer & others",
    }


def test_each_payee_is_coloured_by_its_role():
    tiers = load_deal(DEMO)["tiers"]
    rows = compare_scenarios(tiers, SCENARIOS)
    roles = payee_roles(tiers, EQUITY)
    fig = scenario_bar_chart(rows, list(SCENARIOS), roles)
    for trace in fig.data:
        assert trace.marker.color in ROLE_COLOURS[roles[trace.name]]