import plotly.graph_objects as go


def scenario_bar_chart(rows: list[dict], scenarios: list[str]) -> go.Figure:
    """Stacked bars: one bar per scenario, one coloured block per payee.

    `rows` come from compare_scenarios (amounts in cents). The first payee
    is drawn at the bottom, so reading upward follows the waterfall.
    """
    fig = go.Figure()
    for row in rows:
        fig.add_trace(go.Bar(
            name=row["Who"],
            x=scenarios,
            y=[row[label] / 100 for label in scenarios],
            hovertemplate="%{x}: $%{y:,.0f}<extra>" + row["Who"] + "</extra>",
        ))
    fig.update_layout(
        barmode="stack",
        yaxis_title="Dollars paid",
        yaxis_tickprefix="$",
        yaxis_tickformat=",.0f",
        legend_title_text="Paid to (bottom is paid first)",
        legend_traceorder="reversed",
        margin={"t": 30},
    )
    return fig