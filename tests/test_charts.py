from pathlib import Path

import pytest

from charts import scenario_bar_chart
from engine.deal import load_deal
from engine.scenarios import compare_scenarios

DEMO = Path(__file__).parent.parent / "demos" / "reference_deal.json"
SCENARIOS = {"Flop": 40_000_000, "Base": 150_000_000, "Breakout": 400_000_000}


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