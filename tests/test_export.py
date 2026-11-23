from io import BytesIO
from pathlib import Path

from openpyxl import load_workbook

from engine.deal import load_deal
from export import build_workbook

DEMO = Path(__file__).parent.parent / "demos" / "reference_deal.json"
SCENARIOS = {"Flop": 40_000_000, "Base": 150_000_000, "Breakout": 400_000_000}
EQUITY = ["Equity recoupment", "Investor profit share"]


def open_export():
    """Build the workbook, then open it again the way Excel would."""
    tiers = load_deal(DEMO)["tiers"]
    data = build_workbook("Reference deal", tiers, SCENARIOS, EQUITY, 35_000_000)
    return load_workbook(BytesIO(data))


def test_workbook_has_all_four_sheets():
    assert open_export().sheetnames == ["Summary", "Waterfall", "Scenarios", "Equity returns"]


def test_scenarios_sheet_matches_the_excel_reference():
    sheet = open_export()["Scenarios"]
    assert [cell.value for cell in sheet[1]] == ["Who", "Flop", "Base", "Breakout"]
    rows = {row[0].value: [cell.value for cell in row[1:]] for row in sheet.iter_rows(min_row=2)}
    assert rows["Equity recoupment"] == [118_000, 420_000, 420_000]
    assert rows["Total paid"] == ["=SUM(B2:B8)", "=SUM(C2:C8)", "=SUM(D2:D8)"]


def test_equity_sheet_uses_a_live_moic_formula():
    sheet = open_export()["Equity returns"]
    assert sheet["B3"].value == 731_000   # Base scenario, equity received
    assert sheet["D3"].value == "=B3/C3"  # MOIC is a formula, not a typed number