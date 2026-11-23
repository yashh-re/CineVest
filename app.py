from pathlib import Path

import pandas as pd
import streamlit as st

from engine.deal import load_deal
from engine.returns import breakeven_gross, moic
from engine.waterfall import run_waterfall

DEAL_FILE = Path(__file__).parent / "demos" / "reference_deal.json"
EQUITY = ["Equity recoupment", "Investor profit share"]
EQUITY_INVESTED = 35_000_000  # $350,000 in cents

st.set_page_config(page_title="CineVest")
st.title("CineVest")
st.write("See who gets paid back from a film, in what order, and how much.")

deal = load_deal(DEAL_FILE)
st.subheader(deal["title"])

gross_dollars = st.slider(
    "Gross revenue ($)", min_value=0, max_value=5_000_000,
    value=1_500_000, step=10_000,
)
gross = gross_dollars * 100  # the engine works in cents

paid = run_waterfall(gross, deal["tiers"])
table = pd.DataFrame({
    "Who": list(paid.keys()),
    "Paid": [f"${cents / 100:,.2f}" for cents in paid.values()],
})
st.dataframe(table, hide_index=True, use_container_width=True)

received = sum(paid[name] for name in EQUITY)
breakeven = breakeven_gross(deal["tiers"], EQUITY, EQUITY_INVESTED)

col1, col2, col3 = st.columns(3)
col1.metric("Equity received", f"${received / 100:,.0f}")
col2.metric("Equity MOIC", f"{moic(received, EQUITY_INVESTED):.2f}x")
col3.metric("Equity breakeven revenue", f"${breakeven / 100:,.0f}")

st.caption("Illustrative scenario only. Not legal or investment advice.")