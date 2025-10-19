import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from languages import LANGUAGES

lang = LANGUAGES[st.session_state.language]

st.image("ecometer.png", width=100)
st.title(lang["dashboard_title"])

try:
    data_entries = pd.read_csv("data/data_entries.csv")
    co2_factors = pd.read_csv("data/co2_factors.csv")

    # Calculate CO2 emissions
    df = pd.merge(data_entries, co2_factors, on="Activity")
    df["CO2 Emissions"] = df["Quantity"] * df["Factor"]

    # --- Charts in Tabs ---
    tab1, tab2 = st.tabs([lang["emissions_by_activity"], lang["emissions_by_school"]])

    with tab1:
        st.subheader(lang["emissions_by_activity"])
        fig_pie = px.pie(
            df, 
            values='CO2 Emissions', 
            names='Activity', 
            title='Emissions by Activity',
            color_discrete_sequence=['#FF7C32']
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with tab2:
        st.subheader(lang["emissions_by_school"])
        school_emissions = df.groupby("School")["CO2 Emissions"].sum().reset_index()
        
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=school_emissions["School"],
            y=school_emissions["CO2 Emissions"],
            marker_color='#7CC142'
        ))
        
        # Add a line for normal CO2 emissions
        normal_emission_level = 200 # This is an arbitrary value, you can change it
        fig_bar.add_shape(
            type="line",
            x0=-0.5,
            y0=normal_emission_level,
            x1=len(school_emissions["School"]) - 0.5,
            y1=normal_emission_level,
            line=dict(
                color="#FF7C32",
                width=2,
                dash="dashdot",
            ),
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)


    # --- Total Emissions ---
    with st.container():
        st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
        st.subheader(lang["total_emissions"])
        total_emissions = df["CO2 Emissions"].sum()
        st.metric(label="Total CO2 Emissions (kg)", value=f"{total_emissions:.2f}")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Dashboard Suggestions ---
    with st.container():
        st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
        st.subheader(lang["dashboard_suggestions"])
        st.markdown(lang["suggestion_1"])
        st.markdown(lang["suggestion_2"])
        st.markdown(lang["suggestion_3"])
        st.markdown('</div>', unsafe_allow_html=True)

except FileNotFoundError:
    st.warning("No data entries found. Please add data in the Data Entry page.")
