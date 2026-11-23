from pathlib import Path

import pandas as pd
import streamlit as st

from engine.deal import load_deal
from engine.incentives import incentive_amount, load_presets
from engine.returns import breakeven_gross, moic
from engine.stack import stack_summary
from engine.table import COLUMNS, rows_to_tiers, tiers_to_rows
from engine.waterfall import run_waterfall

DEAL_FILE = Path(__file__).parent / "demos" / "reference_deal.json"
TIER_KINDS = ["percent_of_gross", "fixed", "recoup", "share_of_remaining"]
DEFAULT_EQUITY = ["Equity recoupment", "Investor profit share"]

st.set_page_config(page_title="CineVest")
st.title("CineVest")
st.write("See who gets paid back from a film, in what order, and how much.")

deal = load_deal(DEAL_FILE)
presets = load_presets()

# 1. The capital stack: where the budget comes from
st.subheader("1. The capital stack")
st.write("Where the budget comes from. The tax credit counts at its cash value.")

budget_dollars = st.number_input(
    "Production budget ($)", min_value=1, value=1_000_000, step=50_000)

left, right = st.columns(2)
presale_dollars = left.number_input("Presales ($)", min_value=0, value=300_000, step=10_000)
gap_dollars = left.number_input("Gap loan ($)", min_value=0, value=150_000, step=10_000)
equity_dollars = left.number_input("Equity ($)", min_value=0, value=350_000, step=10_000)

state = right.selectbox(
    "Tax credit state",
    options=list(presets["states"].keys()),
    format_func=lambda code: presets["states"][code]["name"],
)
preset = presets["states"][state]
rate_pct = right.slider(
    "Credit rate (%)",
    min_value=int(preset["base_rate"] * 100),
    max_value=int(preset["max_rate"] * 100),
    value=int(preset["base_rate"] * 100),
)
spend_dollars = right.number_input(
    "Qualifying spend in that state ($)",
    min_value=0, value=int(budget_dollars), step=50_000)
credit = incentive_amount(state, spend_dollars * 100, rate=rate_pct / 100, presets=presets)
right.write(f"Credit: ${credit['credit'] / 100:,.0f} face value, "
            f"${credit['cash_value'] / 100:,.0f} in cash")

sources = {
    "Presales": presale_dollars * 100,
    "Tax credit (cash value)": credit["cash_value"],
    "Gap loan": gap_dollars * 100,
    "Equity": equity_dollars * 100,
}
summary = stack_summary(budget_dollars * 100, sources)
st.progress(min(summary["percent_funded"], 1.0),
            text=f"{summary['percent_funded']:.0%} funded")
m1, m2 = st.columns(2)
m1.metric("Funded", f"${summary['funded'] / 100:,.0f}")
if summary["over_funded"]:
    m2.metric("Over budget by", f"${summary['over_funded'] / 100:,.0f}")
else:
    m2.metric("Still needed", f"${summary['still_needed'] / 100:,.0f}")
st.caption(f"{preset['name']} credit rules as of {presets['as_of']}. Source: {preset['source']}")

# 2. The waterfall: an editable table, starting from the reference deal
st.subheader("2. The waterfall")
st.write("Tiers are paid from the lowest Order number up. Edit any cell, "
         "add a row at the bottom, or select a row and delete it.")

starting_rows = pd.DataFrame(tiers_to_rows(deal["tiers"]), columns=COLUMNS)
edited = st.data_editor(
    starting_rows,
    num_rows="dynamic",
    hide_index=True,
    use_container_width=True,
    column_config={
        "Order": st.column_config.NumberColumn(
            "Order", min_value=0, step=0.1, help="Lower numbers are paid first"),
        "Kind": st.column_config.SelectboxColumn("Kind", options=TIER_KINDS),
        "Rate (%)": st.column_config.NumberColumn("Rate (%)", min_value=0, max_value=100),
        "Amount ($)": st.column_config.NumberColumn("Amount ($)", min_value=0, format="$%.2f"),
        "Principal ($)": st.column_config.NumberColumn("Principal ($)", min_value=0, format="$%.2f"),
        "Multiple": st.column_config.NumberColumn("Multiple", min_value=0.0, step=0.01),
    },
)

try:
    tiers = rows_to_tiers(edited.to_dict("records"))
except ValueError as error:
    st.error(str(error))
    st.stop()

# 3. The outcome at one level of revenue
st.subheader("3. The outcome")
gross_dollars = st.slider(
    "Gross revenue ($)", min_value=0, max_value=5_000_000,
    value=1_500_000, step=10_000,
)
gross = gross_dollars * 100  # the engine works in cents

paid = run_waterfall(gross, tiers)
results = pd.DataFrame({
    "Who": list(paid.keys()),
    "Paid": [f"${cents / 100:,.2f}" for cents in paid.values()],
})
st.dataframe(results, hide_index=True, use_container_width=True)

# 4. The equity investors' returns
st.subheader("4. The equity investors")
names = [tier.name for tier in tiers]
equity_names = st.multiselect(
    "Which tiers pay the equity investors?",
    options=names,
    default=[name for name in DEFAULT_EQUITY if name in names],
)
invested = equity_dollars * 100
st.write(f"Equity invested: ${equity_dollars:,.0f} (from the capital stack)")

if equity_names and invested > 0:
    received = sum(paid[name] for name in equity_names)
    col1, col2, col3 = st.columns(3)
    col1.metric("Equity received", f"${received / 100:,.0f}")
    col2.metric("Equity MOIC", f"{moic(received, invested):.2f}x")
    try:
        breakeven = breakeven_gross(tiers, equity_names, invested)
        col3.metric("Equity breakeven revenue", f"${breakeven / 100:,.0f}")
    except ValueError:
        col3.metric("Equity breakeven revenue", "Never")
else:
    st.info("Pick the equity tiers and set an equity amount to see their returns.")

st.caption("Illustrative scenario only. Not legal or investment advice.")