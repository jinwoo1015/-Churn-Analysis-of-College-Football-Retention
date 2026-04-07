import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
import numpy as np

# --- 1. SETUP & CONFIG ---
st.set_page_config(page_title="Flight Risk Dashboard", page_icon="🏈", layout="wide")
st.title("🏈 Transfer Portal Risk Dashboard")
st.markdown("Identify players at high risk of entering the transfer portal based on physical Catapult metrics.")

# --- 2. LOAD MODEL & DATA ---
# Cache the model so it doesn't reload every time the user clicks a button
@st.cache_resource
def load_model():
    with open('transfer_model.pkl', 'rb') as file:
        return pickle.load(file)

model = load_model()

# Create some mock data for the MVP (Replace this with pd.read_csv('your_roster.csv') later!)
df = pd.read_csv('chunn_model_data_repo.csv')

# --- 3. MAKE PREDICTIONS ---
# Get the probability of transferring (Class 1)
features = df[['Avg_Player_Load_Per_Min', 'Season_Max_Velocity', 'homeLatitude']]
df['Risk Score (%)'] = model.predict_proba(features)[:, 1] * 100
df['Risk Score (%)'] = df['Risk Score (%)'].round(1)

# Sort from highest risk to lowest
df = df.sort_values(by='Risk Score (%)', ascending=False).reset_index(drop=True)

# --- 4. BUILD THE DASHBOARD UI ---
st.subheader("Current Roster Status")

# Create a clean layout with columns
col1, col2, col3 = st.columns(3)
col1.metric("Total Players Analyzed", len(df))
col2.metric("High Risk Players (>70%)", len(df[df['Risk Score (%)'] > 70]))
col3.metric("Avg Squad Risk", f"{df['Risk Score (%)'].mean():.1f}%")

st.divider()

st.markdown("### Player Hometowns")

# Add a tiny bit of random noise (approx 1-2 miles) so dots don't stack
df['lat_jitter'] = df['homeLatitude'] + np.random.uniform(-0.02, 0.02, size=len(df))
df['lon_jitter'] = df['homeLongitude'] + np.random.uniform(-0.02, 0.02, size=len(df))

# Create the interactive map using the new jittered columns
fig = px.scatter_mapbox(
    df, 
    lat="lat_jitter", 
    lon="lon_jitter", 
    color="transfer", 
    color_discrete_map={0: "blue", 1: "red"}, 
    hover_name="Name_x", 
    hover_data={"Risk Score (%)": ':.2f', "lat_jitter": False, "lon_jitter": False}, # Hides the messy coordinates from the tooltip
    zoom=3, 
    mapbox_style="carto-darkmatter" 
)

st.plotly_chart(fig, use_container_width=True)

# Display the interactive roster list
st.markdown("### 📋 Roster Risk Breakdown")

# 1. Create two columns for our sorting and filtering dropdowns so they sit side-by-side
filter_col, sort_col = st.columns(2)

with filter_col:
    # Grab all unique positions from the dataset and add an "All" option
    # (Make sure your column is actually named 'Position' in your CSV!)
    all_positions = ['All'] + list(df['position'].unique())
    selected_position = st.selectbox("Filter by Position:", all_positions)

with sort_col:
    # Create sorting options
    sort_option = st.selectbox(
        "Sort Roster By:", 
        ["Risk: High to Low", "Risk: Low to High", "Name: A to Z"]
    )

# 2. Apply the Position Filter
if selected_position != 'All':
    display_df = df[df['position'] == selected_position]
else:
    display_df = df.copy()

# 3. Apply the Sorting Logic
if sort_option == "Risk: High to Low":
    display_df = display_df.sort_values(by="Risk Score (%)", ascending=False)
elif sort_option == "Risk: Low to High":
    display_df = display_df.sort_values(by="Risk Score (%)", ascending=True)
elif sort_option == "Name: A to Z":
    display_df = display_df.sort_values(by="Name_x", ascending=True)


table_df = display_df[['Name_x', 'position', 'Risk Score (%)', 'Avg_Player_Load_Per_Min', 'Season_Max_Velocity', 'homeLatitude']].copy()

# Round the numerical columns so they look clean in the table
table_df['Avg_Player_Load_Per_Min'] = table_df['Avg_Player_Load_Per_Min'].round(2)
table_df['Season_Max_Velocity'] = table_df['Season_Max_Velocity'].round(2)
table_df['homeLatitude'] = table_df['homeLatitude'].round(2)

# 5. Display the Interactive Heatmap Table
st.dataframe(
    # Apply a red color gradient specifically to the Risk Score column
    table_df.style.background_gradient(cmap='Reds', subset=['Risk Score (%)']),
    use_container_width=True,
    hide_index=True, # Hides the ugly row numbers (0, 1, 2...)
    height=400 # Keeps the table a manageable size so they can scroll inside it
)