import streamlit as st
import pandas as pd
import os
from languages import LANGUAGES
from dotenv import load_dotenv

load_dotenv()

# --- App Setup ---
def setup_app():
    """Initializes the app environment, creating data directory and default files."""
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists("data/co2_factors.csv"):
        co2_factors = pd.DataFrame({
            "Activity": ["Electricity", "Paper", "Plastic", "Food/Waste", "Transport"],
            "Factor": [0.5, 0.1, 1.2, 0.8, 0.2]
        })
        co2_factors.to_csv("data/co2_factors.csv", index=False)

setup_app()

st.set_page_config(
    page_title="EcoMeter for Schools",
    page_icon="ecometer.png",
    layout="wide",
)

# Inject custom CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Language Selection ---
def get_language():
    """Gets the selected language from the session state."""
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

# --- Data Entry Form ---
with st.form("data_entry_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        try:
            schools = pd.read_csv("data/schools.csv")
            school_options = schools["School"].tolist()
            school = st.selectbox(lang["school"], school_options, key="school")
            is_school_selected = bool(school_options)
        except FileNotFoundError:
            st.warning("No schools found. Please add schools on the Admin page.")
            school = ""
            is_school_selected = False

    with col2:
        activity_type = st.selectbox(
            lang["activity_type"],
            [lang["electricity"], lang["paper"], lang["plastic"], lang["food_waste"], lang["transport"]],
            key="activity_type"
        )

    with col3:
        quantity = st.number_input(lang["quantity"], min_value=0.0, format="%.2f", key="quantity")

    # Disable submit button if no school is selected
    submitted = st.form_submit_button(lang["submit"], disabled=not is_school_selected)
    if submitted:
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

# --- Form Reset ---
def reset_form():
    """Resets the data entry form fields."""
    st.session_state.school = ""
    st.session_state.activity_type = lang["electricity"]
    st.session_state.quantity = 0.0

st.button(lang["reset"], on_click=reset_form)
