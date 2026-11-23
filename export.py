from io import BytesIO

from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

from engine.returns import received_by
from engine.scenarios import compare_scenarios
from engine.table import COLUMNS, tiers_to_rows

MONEY = '"$"#,##0.00'
MULTIPLE = '0.00"x"'
BOLD = Font(bold=True)


def build_workbook(title: str, tiers: list, scenarios: dict[str, int],
                   equity_names: list[str], invested: int) -> bytes:
    """Build an Excel workbook of the deal. Amounts come in as cents, go out as dollars."""
    workbook = Workbook()
    labels = list(scenarios)

    # Summary
    summary = workbook.active
    summary.title = "Summary"
    summary.append([title])
    summary["A1"].font = Font(bold=True, size=14)
    summary.append(["Amounts in US dollars. Illustrative scenario only. "
                    "Not legal or investment advice."])
    summary.append([])
    summary.append(["Made with CineVest", "https://cinevest.streamlit.app"])

    # Waterfall: the tiers, as shown in the app's table
    waterfall = workbook.create_sheet("Waterfall")
    waterfall.append(COLUMNS)
    for row in tiers_to_rows(tiers):
        waterfall.append([row[column] for column in COLUMNS])

    # Scenarios: who got paid what, with live SUM totals
    scenario_sheet = workbook.create_sheet("Scenarios")
    scenario_sheet.append(["Who"] + labels)
    rows = compare_scenarios(tiers, scenarios)
    for row in rows:
        scenario_sheet.append([row["Who"]] + [row[label] / 100 for label in labels])
    last_row = len(rows) + 1
    totals = ["Total paid"]
    for column in range(2, len(labels) + 2):
        letter = get_column_letter(column)
        totals.append(f"=SUM({letter}2:{letter}{last_row})")
    scenario_sheet.append(totals)
    scenario_sheet.append(["Gross revenue"] + [scenarios[label] / 100 for label in labels])

    # Equity returns, with a live MOIC formula
    equity = workbook.create_sheet("Equity returns")
    equity.append(["Scenario", "Equity received", "Equity invested", "MOIC"])
    for excel_row, label in enumerate(labels, start=2):
        received = received_by(scenarios[label], tiers, equity_names)
        equity.append([label, received / 100, invested / 100,
                       f"=B{excel_row}/C{excel_row}"])

    # Formatting: bold headers, wide first column, money and multiple formats
    for sheet in (waterfall, scenario_sheet, equity):
        for cell in sheet[1]:
            cell.font = BOLD
        sheet.column_dimensions["A"].width = 26
    for row in scenario_sheet.iter_rows(min_row=2, min_col=2):
        for cell in row:
            cell.number_format = MONEY
    for row in equity.iter_rows(min_row=2, min_col=2, max_col=3):
        for cell in row:
            cell.number_format = MONEY
    for row in equity.iter_rows(min_row=2, min_col=4, max_col=4):
        for cell in row:
            cell.number_format = MULTIPLE

    buffer = BytesIO()
    workbook.save(buffer)
    return buffer.getvalue()