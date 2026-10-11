"""Plotly figures, themed to match assets/style.css."""
import plotly.express as px
import plotly.graph_objects as go

CHALK, DIM, GRID = "#ece8dc", "#8a948d", "#1e2924"
EMBER, TEAL = "#ff6a3d", "#3ddc97"
RISK_SCALE = [[0, "#2f7d62"], [0.5, "#d9c46a"], [1, "#ff4d2e"]]
FONT = dict(family="Hanken Grotesk, sans-serif", color=CHALK, size=13)


def _theme(fig: go.Figure, height: int) -> go.Figure:
    fig.update_layout(
        height=height, font=FONT, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=8, b=0),
        legend=dict(orientation="h", y=1.08, x=0, title=None, font=dict(color=DIM)),
        hoverlabel=dict(bgcolor="#0b100e", bordercolor=GRID, font=FONT),
    )
    return fig


def hometown_map(df, color_by: str) -> go.Figure:
    hover = {"risk": ":.1f", "lat": False, "lon": False, "position": True, "hometown": True}
    center = dict(lat=df["lat"].median(), lon=df["lon"].median())
    common = dict(lat="lat", lon="lon", hover_name="name", hover_data=hover, center=center, zoom=3, map_style="carto-darkmatter")
    if color_by == "Risk score":
        fig = px.scatter_map(df, color="risk", size="risk", size_max=16, color_continuous_scale=RISK_SCALE,
                             range_color=(0, 100), **common)
        fig.update_layout(coloraxis_colorbar=dict(title=None, thickness=8, len=0.5, x=0.01, y=0.3,
                                                  tickfont=dict(color=DIM, size=11)))
    else:
        fig = px.scatter_map(df, color="outcome", size="risk", size_max=16,
                             color_discrete_map={"Transferred": EMBER, "Stayed": TEAL},
                             category_orders={"outcome": ["Transferred", "Stayed"]}, **common)
    fig.update_traces(marker=dict(opacity=0.85), selector=dict(type="scattermap"))
    return _theme(fig, 520)


def risk_distribution(df, threshold: float) -> go.Figure:
    fig = go.Figure()
    for outcome, color in (("Stayed", TEAL), ("Transferred", EMBER)):
        fig.add_histogram(x=df.loc[df["outcome"] == outcome, "risk"], name=outcome, marker_color=color,
                          xbins=dict(start=0, end=100, size=5), opacity=0.9)
    fig.add_vline(x=threshold, line=dict(color=CHALK, width=1, dash="dot"),
                  annotation_text=f"alert ≥ {threshold:g}", annotation_font=dict(color=DIM, size=11))
    fig.update_layout(barmode="stack", bargap=0.12)
    fig.update_xaxes(title=None, range=[0, 102], ticksuffix="%", gridcolor=GRID, zeroline=False)
    fig.update_yaxes(title=None, gridcolor=GRID, zeroline=False)
    return _theme(fig, 300)


def risk_by_position(df) -> go.Figure:
    pos = df.groupby("position")["risk"].mean().sort_values().round(1)
    fig = go.Figure(go.Bar(
        x=pos.values, y=pos.index, orientation="h", text=[f"{v:.1f}" for v in pos.values],
        textposition="outside", textfont=dict(color=DIM, size=12), cliponaxis=False,
        marker=dict(color=pos.values, colorscale=RISK_SCALE, cmin=0, cmax=100), hovertemplate="%{y}: %{x:.1f}%<extra></extra>",
    ))
    fig.update_xaxes(range=[0, 100], showgrid=True, gridcolor=GRID, ticksuffix="%", zeroline=False)
    fig.update_yaxes(title=None)
    fig.update_layout(bargap=0.35, showlegend=False)
    return _theme(fig, 300)
