import streamlit as st

from dashboard import charts, ui
from dashboard.data import load_roster

st.set_page_config(page_title="Flight Risk · Roster Retention", page_icon="🏈", layout="wide")
ui.inject_css()

roster = load_roster()

with st.sidebar:
    st.markdown("### Controls")
    threshold = st.slider("Alert threshold (%)", 30, 95, 70, step=5)
    positions = st.multiselect("Positions", sorted(roster["position"].unique()), placeholder="All positions")
    query = st.text_input("Find player", placeholder="Player12")

view = roster
if positions:
    view = view[view["position"].isin(positions)]
if query:
    view = view[view["name"].str.contains(query, case=False, regex=False)]

ui.masthead(len(roster))
if view.empty:
    st.info("No players match these filters.")
    st.stop()

ui.kpis(view, threshold)

ui.section("01", "Where they come from")
map_col, list_col = st.columns([7, 4], gap="medium")
with map_col:
    color_by = st.segmented_control("Colour by", ["Risk score", "Actual outcome"], default="Risk score", label_visibility="collapsed")
    st.plotly_chart(charts.hometown_map(view, color_by or "Risk score"), width="stretch", config={"displayModeBar": False})
with list_col:
    ui.watchlist(view)

ui.section("02", "How the model sees the roster")
dist_col, pos_col = st.columns(2, gap="medium")
with dist_col:
    st.caption("RISK SCORE DISTRIBUTION · BY ACTUAL OUTCOME")
    st.plotly_chart(charts.risk_distribution(view, threshold), width="stretch", config={"displayModeBar": False})
with pos_col:
    st.caption("AVERAGE RISK · BY POSITION")
    st.plotly_chart(charts.risk_by_position(view), width="stretch", config={"displayModeBar": False})

ui.section("03", "Full roster")
st.dataframe(
    view[["name", "position", "risk", "outcome", "Avg_Player_Load_Per_Min", "Season_Max_Velocity", "hometown"]],
    hide_index=True, width="stretch", height=420,
    column_config={
        "name": "Player", "position": "Pos",
        "risk": st.column_config.ProgressColumn("Risk", min_value=0, max_value=100, format="%.1f%%"),
        "outcome": "Actual",
        "Avg_Player_Load_Per_Min": st.column_config.NumberColumn("Load / min", format="%.2f"),
        "Season_Max_Velocity": st.column_config.NumberColumn("Max velocity", format="%.1f"),
        "hometown": "Hometown",
    },
)
