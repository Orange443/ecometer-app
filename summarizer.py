# summarizer.py

import os
from groq import Groq

def get_summary(data: str) -> str:
    """Generates a summary of the given data using the Groq API."""

    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    prompt = f"""Please summarize the following data from the EcoMeter for Schools app. 
    The summary should be easy for students and teachers to understand. 
    Highlight key trends and insights.

    Data:
    {data}
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="openai/gpt-oss-120b",
    )

    return chat_completion.choices[0].message.content
