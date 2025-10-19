import streamlit as st
import pandas as pd
from languages import LANGUAGES
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="EcoMeter for Schools",
    page_icon="ecometer.png",
    layout="wide",
)

# Inject custom CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def get_language():
    if 'language' not in st.session_state:
        st.session_state.language = "English"

    language_name = st.sidebar.selectbox(
        "Language / ભાષા", 
        options=list(LANGUAGES.keys()), 
        index=list(LANGUAGES.keys()).index(st.session_state.language)
    )
    st.session_state.language = language_name
    return LANGUAGES[language_name]

lang = get_language()

st.title(lang["data_entry_page"])

st.sidebar.success(lang["select_page"])

with st.form("data_entry_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        try:
            schools = pd.read_csv("data/schools.csv")
            school = st.selectbox(lang["school"], schools["School"], key="school")
        except FileNotFoundError:
            st.warning("No schools found. Please add schools in the admin page.")
            school = ""

    with col2:
        activity_type = st.selectbox(
            lang["activity_type"],
            [lang["electricity"], lang["paper"], lang["plastic"], lang["food_waste"], lang["transport"]],
            key="activity_type"
        )

    with col3:
        quantity = st.number_input(lang["quantity"], min_value=0.0, format="%.2f", key="quantity")

    submitted = st.form_submit_button(lang["submit"])
    if submitted:
        if school:
            try:
                co2_factors = pd.read_csv("data/co2_factors.csv")
                activity_map = {
                    lang["electricity"]: "Electricity",
                    lang["paper"]: "Paper",
                    lang["plastic"]: "Plastic",
                    lang["food_waste"]: "Food/Waste",
                    lang["transport"]: "Transport",
                }
                activity_english = activity_map[activity_type]
                factor = co2_factors.loc[co2_factors['Activity'] == activity_english, 'Factor'].iloc[0]
                points = int(quantity * factor * 10)
                new_entry = pd.DataFrame([{"Activity": activity_english, "Quantity": quantity, "School": school, "Verified": False}])
                try:
                    data_entries = pd.read_csv("data/data_entries.csv")
                    data_entries = pd.concat([data_entries, new_entry], ignore_index=True)
                except FileNotFoundError:
                    data_entries = new_entry
                data_entries.to_csv("data/data_entries.csv", index=False)
                st.success(f"{lang['success_message']} You've earned {points} points! 🎉")
            except (FileNotFoundError, IndexError):
                st.error("CO2 factors not found. Please configure them in the data folder.")

if st.button(lang["reset"]):
    st.session_state.school = ""
    st.session_state.activity_type = lang["electricity"]
    st.session_state.quantity = 0.0
