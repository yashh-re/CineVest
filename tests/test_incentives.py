import pytest

from engine.incentives import incentive_amount, load_presets


def usd(dollars):
    return dollars * 100


def test_indiana_base_credit_matches_reference_deal():
    result = incentive_amount("IN", usd(1_000_000))
    assert result["credit"] == usd(200_000)
    assert result["cash_value"] == usd(180_000)


def test_indiana_credit_is_capped_at_250k():
    assert incentive_amount("IN", usd(2_000_000))["credit"] == usd(250_000)


def test_georgia_at_max_rate():
    result = incentive_amount("GA", usd(1_000_000), rate=0.30)
    assert result["credit"] == usd(300_000)
    assert result["cash_value"] == usd(270_000)


def test_refundable_credit_has_no_broker_discount():
    result = incentive_amount("NM", usd(1_000_000))
    assert result["cash_value"] == result["credit"] == usd(250_000)


def test_rate_above_state_maximum_is_rejected():
    with pytest.raises(ValueError):
        incentive_amount("IN", usd(1_000_000), rate=0.35)


def test_unknown_state_is_rejected():
    with pytest.raises(ValueError):
        incentive_amount("XX", usd(1_000_000))


def test_every_preset_has_a_source():
    presets = load_presets()
    assert presets["as_of"]
    for code, preset in presets["states"].items():
        assert preset["source"].startswith("https://"), code