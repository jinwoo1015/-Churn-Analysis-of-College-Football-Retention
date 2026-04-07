import streamlit as st
import pandas as pd
import pickle

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

# Display the interactive roster list
for index, row in df.iterrows():
    # Use expanders so coaches can click a player to see "Why"
    with st.expander(f"**{row['Name_x']}** - Risk: {row['Risk Score (%)']:.1f}%"):
        
        # Color code the warning based on risk level
        if row['Risk Score (%)'] > 70:
            st.error("🚨 HIGH FLIGHT RISK - Immediate Intervention Recommended")
        elif row['Risk Score (%)'] > 30:
            st.warning("⚠️ MEDIUM FLIGHT RISK - Monitor closely")
        else:
            st.success("✅ LOW FLIGHT RISK")
            
        st.markdown("#### Driver Metrics:")
        c1, c2, c3 = st.columns(3)
        c1.metric("Avg Load / Min", row['Avg_Player_Load_Per_Min'])
        c2.metric("Max Velocity", row['Season_Max_Velocity'])
        c3.metric("Home Latitude", row['homeLatitude'])