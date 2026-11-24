import plotly.graph_objects as go

from engine.models import Tier

# A family of shades per role, so blocks with the same role look related
# but neighbouring blocks can still be told apart.
ROLE_COLOURS = {
    "Fees & costs": ["#71717A", "#52525B", "#A1A1AA", "#3F3F46"],
    "Lenders": ["#7DD3FC", "#38BDF8", "#BAE6FD", "#0EA5E9"],
    "Investors": ["#7B6CF6", "#9D92F8", "#5B4BE0", "#BDB5FB"],
    "Producer & others": ["#D9E86B", "#E6F09A", "#C2D34F", "#EEF5B8"],
}


def payee_roles(tiers: list, equity_names: list[str]) -> dict[str, str]:
    """Work out each payee's role from its kind of tier and the equity selection."""
    roles = {}
    for tier in tiers:
        tier = tier if isinstance(tier, Tier) else Tier.from_dict(tier)
        if tier.kind == "pari_passu":
            for party in tier.parties:
                roles[party.name] = "Investors" if party.name in equity_names else "Lenders"
        elif tier.name in equity_names:
            roles[tier.name] = "Investors"
        elif tier.kind in ("percent_of_gross", "fixed"):
            roles[tier.name] = "Fees & costs"
        elif tier.kind == "recoup":
            roles[tier.name] = "Lenders"
        else:
            roles[tier.name] = "Producer & others"
    return roles


def scenario_bar_chart(rows: list[dict], scenarios: list[str],
                       roles: dict[str, str] | None = None) -> go.Figure:
    """Stacked bars: one bar per scenario, one coloured block per payee.

    `rows` come from compare_scenarios (amounts in cents). The first payee
    is drawn at the bottom, so reading upward follows the waterfall.
    If `roles` is given, blocks are coloured and grouped by role.
    """
    roles = roles or {}
    shades_used = {role: 0 for role in ROLE_COLOURS}
    fig = go.Figure()
    for row in rows:
        name = row["Who"]
        role = roles.get(name)
        style = {}
        if role in ROLE_COLOURS:
            shades = ROLE_COLOURS[role]
            style["marker_color"] = shades[shades_used[role] % len(shades)]
            style["legendgroup"] = role
            style["legendgrouptitle_text"] = role
            shades_used[role] += 1
        fig.add_trace(go.Bar(
            name=name,
            x=scenarios,
            y=[row[label] / 100 for label in scenarios],
            hovertemplate="%{x}: $%{y:,.0f}<extra>" + name + "</extra>",
            marker_line_color="#1A1A1F",
            marker_line_width=2,
            **style,
        ))
    fig.update_layout(
        barmode="stack",
        yaxis_title="Dollars paid",
        yaxis_tickprefix="$",
        yaxis_tickformat=",.0f",
        legend_title_text="Paid to (bottom is paid first)",
        legend_traceorder="reversed+grouped",
        margin={"t": 30},
    )
    # Dark card to match the app
    fig.update_layout(
        paper_bgcolor="#1A1A1F",
        plot_bgcolor="#1A1A1F",
        font={"family": "Space Grotesk, sans-serif", "color": "#F4F4F5", "size": 14},
        bargap=0.35,
    )
    fig.update_xaxes(showline=True, linecolor="#3F3F46", linewidth=2)
    fig.update_yaxes(showline=True, linecolor="#3F3F46", linewidth=2, gridcolor="#26262D")
    return fig