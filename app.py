
import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64

st.set_page_config(page_title="Grant Finder", layout="centered")
st.title("🔍 Ubuntu Grant Finder")

@st.cache_data
def load_grants():
    return pd.read_csv("grants.csv").to_dict(orient="records")

grants = load_grants()

query = st.text_input("Search for grants by title")
if query:
    filtered = [g for g in grants if query.lower() in g['title'].lower()]
else:
    filtered = grants

st.subheader("Available Grants")
for grant in filtered:
    st.markdown(
        f"**[{grant['title']}]({grant['url']})**  \n"
        f"Source: {grant['source']}  \n"
        f"Summary: {grant['summary']}"
    )

st.subheader("📝 Proposal Generator")
with st.form("proposal_form"):
    name = st.text_input("Your Name")
    project = st.text_area("Project Description")
    budget = st.text_input("Estimated Budget")
    submitted = st.form_submit_button("Generate Proposal")

    if submitted:
        st.markdown("### 📄 Generated Proposal")
        proposal_text = f"My name is {name}, and I propose a project focused on: {project}.\n\nThe estimated budget required is {budget}. I am seeking funding to bring this vision to life."
        st.text(proposal_text)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in proposal_text.split("\n"):
            pdf.cell(200, 10, txt=line, ln=True)
        pdf_output_path = "proposal.pdf"
        pdf.output(pdf_output_path)

        with open(pdf_output_path, "rb") as pdf_file:
            base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
            pdf_display = f'<a href="data:application/octet-stream;base64,{base64_pdf}" download="proposal.pdf">📄 Download Proposal as PDF</a>'
            st.markdown(pdf_display, unsafe_allow_html=True)

st.subheader("📬 Contact Us")
with st.form("contact_form"):
    contact_name = st.text_input("Your Name", key="contact_name")
    contact_email = st.text_input("Your Email")
    contact_message = st.text_area("Your Message")
    contact_submitted = st.form_submit_button("Send Message")

    if contact_submitted:
        st.success("Thank you for reaching out! We'll get back to you soon.")
