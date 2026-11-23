import pytest

from engine.incentives import incentive_amount
from engine.stack import stack_summary


def usd(dollars):
    return dollars * 100


BUDGET = usd(1_000_000)


def test_reference_deal_is_fully_funded_at_face_value():
    summary = stack_summary(BUDGET, {
        "Presales": usd(300_000), "Tax credit": usd(200_000),
        "Gap loan": usd(150_000), "Equity": usd(350_000),
    })
    assert summary["funded"] == BUDGET
    assert summary["still_needed"] == 0
    assert summary["percent_funded"] == 1.0


def test_broker_discount_leaves_a_gap():
    credit_cash = incentive_amount("IN", usd(1_000_000))["cash_value"]  # $180,000
    summary = stack_summary(BUDGET, {
        "Presales": usd(300_000), "Tax credit": credit_cash,
        "Gap loan": usd(150_000), "Equity": usd(350_000),
    })
    assert summary["still_needed"] == usd(20_000)


def test_over_funding_is_reported():
    summary = stack_summary(BUDGET, {"Equity": usd(1_200_000)})
    assert summary["over_funded"] == usd(200_000)
    assert summary["still_needed"] == 0


def test_budget_must_be_positive():
    with pytest.raises(ValueError):
        stack_summary(0, {"Equity": usd(100)})