import streamlit as st
import pandas as pd
import os
from summarizer import get_summary
from languages import LANGUAGES

lang = LANGUAGES[st.session_state.language]

st.title("AI Summarizer")

if "GROQ_API_KEY" not in os.environ:
    st.warning("Please set the GROQ_API_KEY environment variable to use the AI Summarizer.")
else:
    @st.cache_data
    def cached_summary(data):
        return get_summary(data)

    if st.button("Summarize Dashboard Data"):
        try:
            data_entries = pd.read_csv("data/data_entries.csv")
            data_string = data_entries.to_string()
            with st.spinner("Generating summary..."):
                summary = cached_summary(data_string)
                st.subheader("Summary")
                st.write(summary)
        except FileNotFoundError:
            st.warning("No data entries found. Please add data in the Data Entry page.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

st.markdown("### Best Practices")
st.markdown("""- **Caching:** Summaries are cached to avoid redundant API calls and improve performance.
- **Asynchronous Requests:** For more complex applications, consider using asynchronous requests to avoid blocking the Streamlit app.
- **Clear Prompts:** Provide clear and concise prompts to the LLM to get the best results.
- **Local Deployment:** While this example uses an API, you can also run smaller, open-source models locally using libraries like `transformers` and `ctransformers`. However, this requires a powerful computer with a dedicated GPU.
""")
