
import streamlit as st

# Example search result list
results = [
    {"title": "Grant for Education", "url": "https://example.com/grant1", "source": "Gov Portal", "summary": "Supports educational programs."},
    {"title": "Tech Innovation Grant", "url": "https://example.com/grant2", "source": "Innovation Fund", "summary": "Encourages new tech ideas."}
]

# Render results
for grant in results:
    st.markdown(
        f"**[{grant['title']}]({grant['url']})**  \n"
        f"Source: {grant['source']}  \n"
        f"Summary: {grant['summary']}"
    )
