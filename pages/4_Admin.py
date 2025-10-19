import streamlit as st
import pandas as pd
import os
import shutil
from languages import LANGUAGES

st.set_page_config(
    page_title="EcoMeter for Schools",
    page_icon="ecometer.png",
    layout="wide",
)

if "language" not in st.session_state:
    st.session_state.language = "English"

lang = LANGUAGES[st.session_state.language]

st.title(lang["admin_title"])

col1, col2 = st.columns(2)

# --- Manage Schools ---
with col1:
    st.subheader(lang["add_school"])
    school_name = st.text_input(lang["school_name"])
    if st.button(lang["add"]):
        try:
            schools = pd.read_csv("data/schools.csv")
            new_school = pd.DataFrame([{"School": school_name}])
            schools = pd.concat([schools, new_school], ignore_index=True)
            schools.to_csv("data/schools.csv", index=False)
            st.success(lang["school_added"])
        except FileNotFoundError:
            pd.DataFrame([{"School": school_name}]).to_csv(
                "data/schools.csv", index=False
            )
            st.success(lang["school_added"])

    st.subheader(lang["remove_school"])
    try:
        schools = pd.read_csv("data/schools.csv")
        school_to_remove = st.selectbox("Select school to remove", schools["School"])
        if st.button(lang["remove"]):
            schools = schools[schools["School"] != school_to_remove]
            schools.to_csv("data/schools.csv", index=False)
            st.success(lang["school_removed"])
    except FileNotFoundError:
        st.warning("No schools to remove.")

# --- Manage Data Entries ---
with col2:
    st.subheader(lang["download_data"])

    @st.cache_data
    def convert_df_to_csv(df):
        return df.to_csv().encode("utf-8")

    try:
        data_entries = pd.read_csv("data/data_entries.csv")
        st.download_button(
            label=lang["download_data"],
            data=convert_df_to_csv(data_entries),
            file_name="data_entries.csv",
            mime="text/csv",
        )
    except FileNotFoundError:
        st.warning("No data to download.")

    st.subheader(lang["clear_entries"])
    if st.button(lang["clear_entries"]):
        if st.checkbox(lang["clear_entries_confirmation"]):
            try:
                data_folder = "data"
                if os.path.exists(data_folder):
                    for filename in os.listdir(data_folder):
                        file_path = os.path.join(data_folder, filename)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                    st.cache_data.clear()  # Clear Streamlit cache for fresh reload
                    st.success(lang["all_entries_cleared"])
                else:
                    st.warning("Data folder not found. Nothing to clear.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

st.markdown("--- ")

st.subheader(lang["verify_data"])
try:
    data_entries = pd.read_csv("data/data_entries.csv")
    st.dataframe(data_entries)
    entry_to_verify = st.selectbox("Select entry to verify", data_entries.index)
    if st.button("Verify"):
        data_entries.loc[entry_to_verify, "Verified"] = True
        data_entries.to_csv("data/data_entries.csv", index=False)
        st.success("Entry verified!")
except FileNotFoundError:
    st.warning("No data entries found.")
