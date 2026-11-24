import streamlit as st

NEOBRUTAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Bebas+Neue&family=Space+Grotesk:wght@400;500;700&display=swap');

:root {
  --ink: #0E0E10;
  --card: #1A1A1F;
  --line: #2E2E36;
  --text: #F4F4F5;
  --muted: #A1A1AA;
  --purple: #7B6CF6;
  --lime: #D9E86B;
}

/* Readable body font everywhere text appears (icons keep their own font) */
.stApp, .stApp p, .stApp li, .stApp label, .stApp input, .stApp textarea,
.stApp button p {
  font-family: 'Space Grotesk', sans-serif !important;
}

/* ---------- Hero ---------- */
.cv-hero { margin: 0.5rem 0 1.25rem 0; }
.cv-title {
  font-family: 'Archivo Black', sans-serif;
  font-size: clamp(3rem, 9vw, 5.5rem);
  line-height: 1;
  letter-spacing: -2px;
  color: var(--lime);
}
.cv-spark { color: var(--text); margin-left: 0.15em; font-size: 0.6em; vertical-align: middle; }
.cv-pill {
  display: inline-block;
  margin: 14px 0 6px 4px;
  padding: 4px 16px;
  background: var(--text);
  color: var(--ink);
  border-radius: 999px;
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 700;
  transform: rotate(-3deg);
  box-shadow: 3px 3px 0 var(--purple);
}
.cv-tagline { color: var(--muted); font-size: 1.15rem; margin: 10px 0 0 0; }

/* Ticker band */
.cv-band {
  overflow: hidden;
  background: var(--purple);
  transform: rotate(-1.5deg);
  margin: 6px 0 28px 0;
  padding: 8px 0;
  border-radius: 6px;
}
.cv-band-track {
  display: inline-block;
  white-space: nowrap;
  animation: cv-scroll 40s linear infinite;
  font-family: 'Bebas Neue', sans-serif;
  font-size: 1.6rem;
  letter-spacing: 1px;
  color: var(--text);
}
.cv-band-track span { margin: 0 18px; }
@keyframes cv-scroll { from { transform: translateX(0); } to { transform: translateX(-50%); } }
@media (prefers-reduced-motion: reduce) { .cv-band-track { animation: none; } }

/* ---------- Section headings: Bebas Neue with a lime underline ---------- */
.stApp h3 {
  font-family: 'Bebas Neue', sans-serif !important;
  font-weight: 400 !important;
  font-size: 2.4rem !important;
  letter-spacing: 1px;
  color: var(--text) !important;
  margin: 2.75rem 0 0.75rem 0 !important;
  padding: 0 !important;
}
.stApp h3::after {
  content: "";
  display: block;
  width: 56px;
  height: 5px;
  margin-top: 6px;
  background: var(--lime);
  border-radius: 999px;
}

/* ---------- Cards: quiet borders, rounded ---------- */
.stApp [data-testid="stMetric"],
.stApp [data-testid="stDataFrame"],
.stApp [data-testid="stPlotlyChart"],
.stApp [data-testid="stFileUploaderDropzone"],
.stApp [data-testid="stAlert"] {
  background: var(--card);
  border: 1.5px solid var(--line) !important;
  border-radius: 18px !important;
}
.stApp [data-testid="stPlotlyChart"] { padding: 8px; }

/* Metrics: the one place the hard purple shadow appears */
.stApp [data-testid="stMetric"] {
  padding: 14px 20px;
  box-shadow: 4px 4px 0 var(--purple);
}
.stApp [data-testid="stMetricValue"] {
  font-family: 'Archivo Black', sans-serif !important;
  color: var(--lime);
}

/* Inputs and dropdowns: just rounder */
.stApp [data-baseweb="input"],
.stApp [data-baseweb="select"] > div {
  border-radius: 12px !important;
}

/* ---------- Buttons: lime pills ---------- */
.stApp .stButton button,
.stApp [data-testid="stDownloadButton"] button,
.stApp [data-testid="stFileUploaderDropzone"] button {
  background: var(--lime) !important;
  color: var(--ink) !important;
  border: none !important;
  border-radius: 999px !important;
  padding: 0.45rem 1.3rem !important;
  box-shadow: 3px 3px 0 var(--purple) !important;
  transition: transform 0.1s, box-shadow 0.1s;
}
.stApp .stButton button p,
.stApp [data-testid="stDownloadButton"] button p,
.stApp [data-testid="stFileUploaderDropzone"] button span {
  color: var(--ink) !important;
  font-weight: 700 !important;
}
.stApp .stButton button:hover,
.stApp [data-testid="stDownloadButton"] button:hover {
  transform: translate(1px, 1px);
  box-shadow: 2px 2px 0 var(--purple) !important;
}

/* ---------- Multiselect tags: purple pills ---------- */
.stApp [data-baseweb="tag"] {
  background: var(--purple) !important;
  border-radius: 999px !important;
}
.stApp [data-baseweb="tag"] span { color: var(--text) !important; font-weight: 700; }
/* ---------- About page: step cards ---------- */
.cv-card {
  background: var(--card);
  border: 1.5px solid var(--line);
  border-radius: 18px;
  padding: 18px 18px 6px 18px;
  height: 100%;
}
.cv-step {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 2.2rem;
  line-height: 1;
  color: var(--lime);
}
.cv-card-title {
  font-family: 'Archivo Black', sans-serif;
  font-size: 1.05rem;
  margin: 6px 0 6px 0;
}
.cv-card p { color: var(--muted); font-size: 0.95rem; }
</style>
"""

BAND_WORDS = ["CAM fee", "Sales agent", "Gap loan", "Tax credit", "Equity",
              "Deferments", "Backend", "Profit split"]


def apply_style() -> None:
    """Inject the style sheet into the page."""
    st.markdown(NEOBRUTAL_CSS, unsafe_allow_html=True)


def render_hero() -> None:
    """The title, a tilted pill, the tagline, and a scrolling band of waterfall terms."""
    items = "✦".join(f"<span>{word.upper()}</span>" for word in BAND_WORDS)
    track = items + "✦" + items + "✦"  # twice, so the scroll loops seamlessly
    st.markdown(
        f"""
        <div class="cv-hero">
          <div class="cv-title">CineVest<span class="cv-spark">✦</span></div>
          <div class="cv-pill">film finance, made readable</div>
          <p class="cv-tagline">See who gets paid back from a film, in what order, and how much.</p>
        </div>
        <div class="cv-band"><div class="cv-band-track">{track}</div></div>
        """,
        unsafe_allow_html=True,
    )