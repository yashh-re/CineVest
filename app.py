from pathlib import Path

import pandas as pd
import streamlit as st

from engine.deal import load_deal
from engine.returns import breakeven_gross, moic
from engine.table import COLUMNS, rows_to_tiers, tiers_to_rows
from engine.waterfall import run_waterfall

DEAL_FILE = Path(__file__).parent / "demos" / "reference_deal.json"
TIER_KINDS = ["percent_of_gross", "fixed", "recoup", "share_of_remaining"]
DEFAULT_EQUITY = ["Equity recoupment", "Investor profit share"]

st.set_page_config(page_title="CineVest")
st.title("CineVest")
st.write("See who gets paid back from a film, in what order, and how much.")

deal = load_deal(DEAL_FILE)

# 1. The waterfall: an editable table, starting from the reference deal
st.subheader("1. The waterfall")
st.write("Tiers are paid from the top down. Edit any cell, add a row at the bottom, "
         "or select a row and delete it.")

starting_rows = pd.DataFrame(tiers_to_rows(deal["tiers"]), columns=COLUMNS)
edited = st.data_editor(
    starting_rows,
    num_rows="dynamic",
    hide_index=True,
    use_container_width=True,
    column_config={
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

# 2. The outcome at one level of revenue
st.subheader("2. The outcome")
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

# 3. The equity investors' returns
st.subheader("3. The equity investors")
names = [tier.name for tier in tiers]
equity_names = st.multiselect(
    "Which tiers pay the equity investors?",
    options=names,
    default=[name for name in DEFAULT_EQUITY if name in names],
)
invested_dollars = st.number_input(
    "Amount the equity investors put in ($)",
    min_value=0, value=350_000, step=10_000,
)
invested = invested_dollars * 100

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
    st.info("Pick the equity tiers and the amount invested to see their returns.")

st.caption("Illustrative scenario only. Not legal or investment advice.")