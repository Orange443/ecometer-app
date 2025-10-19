import streamlit as st
import pandas as pd
from languages import LANGUAGES

lang = LANGUAGES[st.session_state.language]

st.title(lang["leaderboard_title"])

try:
    data_entries = pd.read_csv("data/data_entries.csv")
    co2_factors = pd.read_csv("data/co2_factors.csv")

    # Calculate CO2 emissions
    df = pd.merge(data_entries, co2_factors, on="Activity")
    df["CO2 Emissions"] = df["Quantity"] * df["Factor"]

    # Create leaderboard
    leaderboard = df.groupby("School")["CO2 Emissions"].sum().reset_index()
    leaderboard = leaderboard.sort_values(by="CO2 Emissions", ascending=True)
    leaderboard[lang["rank"]] = range(1, len(leaderboard) + 1)
    leaderboard.loc[leaderboard[lang["rank"]] == 1, lang["rank"]] = "🥇"
    leaderboard.loc[leaderboard[lang["rank"]] == 2, lang["rank"]] = "🥈"
    leaderboard.loc[leaderboard[lang["rank"]] == 3, lang["rank"]] = "🥉"

    col1, col2, col3 = st.columns(3)

    if len(leaderboard) > 0:
        with col1:
            st.subheader(f"{leaderboard.iloc[0][lang['rank']]} {leaderboard.iloc[0]['School']}")
            st.metric(label=lang["co2_emissions"], value=f"{leaderboard.iloc[0]['CO2 Emissions']:.2f} kg")

    if len(leaderboard) > 1:
        with col2:
            st.subheader(f"{leaderboard.iloc[1][lang['rank']]} {leaderboard.iloc[1]['School']}")
            st.metric(label=lang["co2_emissions"], value=f"{leaderboard.iloc[1]['CO2 Emissions']:.2f} kg")

    if len(leaderboard) > 2:
        with col3:
            st.subheader(f"{leaderboard.iloc[2][lang['rank']]} {leaderboard.iloc[2]['School']}")
            st.metric(label=lang["co2_emissions"], value=f"{leaderboard.iloc[2]['CO2 Emissions']:.2f} kg")

    st.dataframe(leaderboard.set_index(lang["rank"]))

except FileNotFoundError:
    st.warning("No data entries found. Please add data in the Data Entry page.")
