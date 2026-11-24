from pathlib import Path

import pytest

from engine.deal import deal_from_json
from engine.waterfall import run_waterfall

DEMOS_DIR = Path(__file__).parent.parent / "demos"
DEMO_FILES = sorted(DEMOS_DIR.glob("*.json"))


def test_there_are_three_demos():
    assert len(DEMO_FILES) == 3


@pytest.mark.parametrize("path", DEMO_FILES, ids=lambda p: p.stem)
def test_demo_is_a_valid_deal(path):
    deal = deal_from_json(path.read_text(encoding="utf-8"))
    assert deal["title"]
    assert deal["description"]
    assert set(deal["scenarios"]) == {"flop", "base", "breakout"}


@pytest.mark.parametrize("path", DEMO_FILES, ids=lambda p: p.stem)
def test_demo_pays_out_every_dollar(path):
    deal = deal_from_json(path.read_text(encoding="utf-8"))
    for gross in deal["scenarios"].values():
        assert sum(run_waterfall(gross, deal["tiers"]).values()) == gross