import streamlit as st
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

st.title(lang["app_header"])

st.sidebar.success("Select a page above.")

st.markdown(f"### {lang['how_to_toggle_themes']}")
st.markdown(f"1. {lang['theme_instructions_1']}")
st.markdown(f"2. {lang['theme_instructions_2']}")
st.markdown(f"3. {lang['theme_instructions_3']}")

st.markdown(f"### {lang['how_to_update_language']}")
st.markdown(f"1. {lang['language_instructions_1']}")
st.markdown(f"2. {lang['language_instructions_2']}")
st.markdown(f"3. {lang['language_instructions_3']}")