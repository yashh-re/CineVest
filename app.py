import streamlit as st

from styles import apply_style

st.set_page_config(page_title="CineVest")
apply_style()

pages = [
    st.Page("views/model.py", title="Model a deal", default=True),
    st.Page("views/about.py", title="About"),
]
st.navigation(pages, position="top").run()