from pathlib import Path

from engine.deal import load_deal, save_deal
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