
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Grant Finder", layout="centered")

st.title("🔍 Ubuntu Grant Finder")

# Load grants from CSV
@st.cache_data
def load_grants():
    return pd.read_csv("grants.csv").to_dict(orient="records")

grants = load_grants()

# Search bar
query = st.text_input("Search for grants by title")
if query:
    filtered = [g for g in grants if query.lower() in g['title'].lower()]
else:
    filtered = grants

# Display grants
st.subheader("Available Grants")
for grant in filtered:
    st.markdown(
        f"**[{grant['title']}]({grant['url']})**  
"
        f"Source: {grant['source']}  
"
        f"Summary: {grant['summary']}"
    )

# Proposal Generator Form
st.subheader("📝 Proposal Generator")
with st.form("proposal_form"):
    name = st.text_input("Your Name")
    project = st.text_area("Project Description")
    budget = st.text_input("Estimated Budget")
    submitted = st.form_submit_button("Generate Proposal")

    if submitted:
        st.markdown("### 📄 Generated Proposal")
        st.write(f"My name is {name}, and I propose a project focused on: {project}.")
        st.write(f"The estimated budget required is {budget}. I am seeking funding to bring this vision to life.")
