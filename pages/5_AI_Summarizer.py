import streamlit as st
import pandas as pd
import os
from summarizer import get_summary
from languages import LANGUAGES

if 'language' not in st.session_state:
    st.session_state.language = 'English'

lang = LANGUAGES[st.session_state.language]

st.title(lang["ai_summarizer_title"])

if "GROQ_API_KEY" not in os.environ:
    st.warning("Please set the GROQ_API_KEY environment variable to use the AI Summarizer.")
else:
    @st.cache_data
    def cached_summary(data, language):
        return get_summary(data, language)

    if st.button("Summarize Dashboard Data"):
        try:
            data_entries = pd.read_csv("data/data_entries.csv")
            data_string = data_entries.to_string()
            with st.spinner("Generating summary..."):
                summary = cached_summary(data_string, st.session_state.language)
                st.subheader("Summary")
                st.write(summary)
        except FileNotFoundError:
            st.warning("No data entries found. Please add data in the Data Entry page.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

st.markdown(f"### {lang['best_practices']}")
st.markdown(lang['caching_tip'])
st.markdown(lang['async_tip'])
st.markdown(lang['prompts_tip'])
st.markdown(lang['local_deployment_tip'])
