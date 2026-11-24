import plotly.graph_objects as go

from engine.models import Tier

# A family of shades per role, so blocks with the same role look related
# but neighbouring blocks can still be told apart.
ROLE_COLOURS = {
    "Fees & costs": ["#9CA3AF", "#6B7280", "#D1D5DB", "#4B5563"],
    "Lenders": ["#3B82F6", "#60A5FA", "#2563EB", "#93C5FD"],
    "Investors": ["#10B981", "#34D399", "#059669", "#6EE7B7"],
    "Producer & others": ["#EAB308", "#FACC15", "#CA8A04", "#FDE047"],
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
    return fig