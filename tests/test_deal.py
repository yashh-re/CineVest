from pathlib import Path

import pytest

from engine.deal import build_deal, deal_from_json, deal_to_json, load_deal, save_deal
from engine.models import Tier
from engine.waterfall import run_waterfall

DEMO = Path(__file__).parent.parent / "demos" / "reference_deal.json"


def test_reference_deal_file_matches_excel():
    deal = load_deal(DEMO)
    paid = run_waterfall(deal["scenarios"]["base"], deal["tiers"])
    assert paid["Equity recoupment"] == 42_000_000  # $420,000
    assert paid["Producer profit share"] == 31_100_000  # $311,000


def test_save_then_load_gives_the_same_deal(tmp_path):
    deal = load_deal(DEMO)
    copy_path = tmp_path / "copy.json"
    save_deal(deal, copy_path)
    assert load_deal(copy_path) == deal

def test_deal_survives_a_round_trip_as_text():
    deal = load_deal(DEMO)
    assert deal_from_json(deal_to_json(deal)) == deal


def test_tiers_from_the_app_can_be_saved():
    tiers = [Tier.from_dict(t) for t in load_deal(DEMO)["tiers"]]
    deal = build_deal("My film", tiers, {"base": 100}, {"budget": 100})
    assert deal["tiers"][3] == {
        "name": "Gap loan", "kind": "recoup",
        "principal": 15_000_000, "multiple": 1.12,
    }


def test_uploaded_file_with_a_typo_is_rejected():
    bad = '{"title": "x", "tiers": [{"name": "Fee", "kind": "fixd", "value": 1}]}'
    with pytest.raises(ValueError, match="fixd"):
        deal_from_json(bad)


def test_uploaded_file_that_is_not_json_is_rejected():
    with pytest.raises(ValueError):
        deal_from_json("this is not json")


def test_uploaded_file_without_tiers_is_rejected():
    with pytest.raises(ValueError, match="tiers"):
        deal_from_json('{"title": "x"}')