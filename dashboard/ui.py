"""HTML fragments and CSS injection. Markup stays single-line so Markdown never treats it as code."""
from html import escape
from pathlib import Path

import streamlit as st

CSS = Path(__file__).resolve().parent.parent / "assets" / "style.css"


def inject_css() -> None:
    st.markdown(f"<style>{CSS.read_text()}</style>", unsafe_allow_html=True)


def masthead(n_players: int) -> None:
    st.markdown(
        '<header class="mast"><div class="eyebrow">Roster retention intelligence</div>'
        '<div class="mast-row"><h1>Flight<br>Risk</h1>'
        '<p class="lede">Which players are most likely to enter the transfer portal, '
        'estimated from Catapult load, top speed and distance from home.</p>'
        f'<ul class="chips"><li>XGBoost</li><li>3 features</li><li>{n_players} players</li></ul></div>'
        '<div class="yardline"></div></header>',
        unsafe_allow_html=True,
    )


def section(num: str, title: str) -> None:
    st.markdown(f'<div class="sec"><span>{num}</span><h2>{escape(title)}</h2><hr></div>', unsafe_allow_html=True)


def kpis(df, threshold: float) -> None:
    hot = df[df["risk"] >= threshold]
    top = df.iloc[0]
    tiles = [
        ("Players in view", f"{len(df)}", "", False),
        (f"At or above {threshold:g}%", f"{len(hot)}", f"{len(hot) / len(df):.0%} of roster", True),
        ("Average risk", f"{df['risk'].mean():.1f}<small>%</small>", "mean transfer probability", False),
        ("Highest risk", f"{top['risk']:.1f}<small>%</small>", f"{escape(top['name'])} · {top['position']}", False),
    ]
    cells = "".join(
        f'<div class="kpi{" hot" if hot_ else ""}" style="animation-delay:{i * 70}ms">'
        f'<span class="kpi-l">{label}</span><span class="kpi-v">{value}</span><span class="kpi-s">{sub or "&nbsp;"}</span></div>'
        for i, (label, value, sub, hot_) in enumerate(tiles)
    )
    st.markdown(f'<div class="kpis">{cells}</div>', unsafe_allow_html=True)


def watchlist(df, n: int = 8) -> None:
    rows = "".join(
        f'<li><span class="rk">{i:02d}</span><span class="who"><b>{escape(r["name"])}</b><i>{r["position"]} · {escape(r["hometown"])}</i></span>'
        f'<span class="bar"><span style="width:{r["risk"]}%"></span></span><span class="sc">{r["risk"]:.0f}</span></li>'
        for i, (_, r) in enumerate(df.head(n).iterrows(), 1)
    )
    st.markdown(f'<div class="panel"><div class="panel-t">Watchlist · top {min(n, len(df))}</div><ol class="wl">{rows}</ol></div>', unsafe_allow_html=True)
