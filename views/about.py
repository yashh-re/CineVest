import streamlit as st

from styles import apply_style

apply_style()

st.markdown(
    '<div class="cv-title" style="font-size:3.5rem">About CineVest'
    '<span class="cv-spark">✦</span></div>'
    '<p class="cv-tagline">A free tool that makes film finance readable.</p>',
    unsafe_allow_html=True,
)

st.subheader("Why it exists")
st.write(
    "An independent film is usually paid for by several people at once: a distributor "
    "that buys the rights early, a state tax credit, a bank or gap lender, and private "
    "investors. When the film earns money, they get paid back in a strict order called "
    "the recoupment waterfall. First-time producers often work this out in fragile "
    "spreadsheets, and their investors can't easily check it. CineVest makes the "
    "waterfall visible, so everyone can see who gets paid, when, and how much, "
    "before the deal is signed."
)

st.subheader("How it works")
steps = [
    ("01", "Build the stack", "Enter presales, a gap loan, equity and a state tax credit. "
                              "See whether the budget is covered."),
    ("02", "Set the waterfall", "List who gets paid, in what order: fees, lenders, "
                                "investors, then the profit split."),
    ("03", "Run the scenarios", "Compare a flop, a base case and a breakout side by side."),
    ("04", "Share the result", "Download an Excel file with live formulas, or save the "
                               "deal to open later."),
]
columns = st.columns(len(steps))
for column, (number, heading, text) in zip(columns, steps):
    column.markdown(
        f'<div class="cv-card"><div class="cv-step">{number}</div>'
        f'<div class="cv-card-title">{heading}</div><p>{text}</p></div>',
        unsafe_allow_html=True,
    )

st.subheader("Who it's for")
st.markdown(
    "- **Independent producers** raising money from several sources, who need to show "
    "investors a clear plan.\n"
    "- **Investors** considering a film, who want to see their downside before they commit.\n"
    "- **Film students** learning how the money side of filmmaking works."
)

st.subheader("Under the hood")
m1, m2, m3 = st.columns(3)
m1.metric("Automated tests", "66")
m2.metric("Random deals checked per run", "1,000")
m3.metric("Demo films", "3")
st.write(
    "The calculations live in a separate Python engine with no screens attached, so "
    "they can be tested on their own. Every result was first worked out by hand in "
    "Excel, money is stored in whole cents to avoid rounding errors, and a "
    "property-based test throws 1,000 random deals at the engine on every run to "
    "prove that no money is ever created or lost. Built with Python, Streamlit, "
    "Plotly and openpyxl."
)

st.subheader("Built by")
st.markdown(
    "Hey! I'm **Yashna**, a junior at Indiana University majoring in Finance and Informatics, with a minor in Film Production. CineVest "
    "sits where those three meet.\n\n"
    "[Source code on GitHub](https://github.com/yashh-re/CineVest)\n\n"
    "Linkedin profile: [Link](https://www.linkedin.com/in/yashnapandugala/)\n\n" 
    "GitHub profile: [Link](https://github.com/yashh-re)"
)

st.subheader("Fine print")
st.caption(
    "CineVest produces illustrative scenarios only. It is not legal or investment "
    "advice. Tax credit rules change often; each preset lists its source and an "
    "as-of date. Check with the state film office before relying on them."
)