import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64
from io import BytesIO
from typing import List, Dict, Any

st.set_page_config(page_title="Grant Finder", layout="centered")
st.title("🔍 Ubuntu Grant Finder")

@st.cache_data
def load_grants() -> List[Dict[str, Any]]:
    """Load and return grants from a CSV file."""
    return pd.read_csv("grants.csv").to_dict(orient="records")

def search_grants(grants: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """Filter grants by matching query in title, summary, or source."""
    q = query.lower()
    return [
        g for g in grants
        if q in g['title'].lower()
        or q in g.get('summary', '').lower()
        or q in g.get('source', '').lower()
    ]

def display_grants(grants: List[Dict[str, Any]]) -> None:
    """Display grants as markdown cards."""
    st.subheader("Available Grants")
    for grant in grants:
        with st.expander(grant['title']):
            st.markdown(
                f"**Source:** {grant['source']}  \n"
                f"**[Grant Link]({grant['url']})**  \n"
                f"**Summary:** {grant['summary']}"
            )

def generate_proposal_pdf(proposal_text: str) -> bytes:
    """Generate a PDF from proposal text and return as bytes."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in proposal_text.split("\n"):
        pdf.cell(200, 10, txt=line, ln=True)
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer.read()

def main():
    grants = load_grants()

    # Grant search
    query = st.text_input("Search for grants by title, summary, or source")
    filtered = search_grants(grants, query) if query else grants
    display_grants(filtered)

    # Proposal generator
    st.subheader("📝 Proposal Generator")
    with st.form("proposal_form"):
        name = st.text_input("Your Name")
        project = st.text_area("Project Description")
        budget = st.text_input("Estimated Budget")
        submitted = st.form_submit_button("Generate Proposal")

        if submitted:
            if not name or not project or not budget:
                st.error("Please fill in all fields.")
            else:
                st.markdown("### 📄 Generated Proposal")
                proposal_text = (
                    f"My name is {name}, and I propose a project focused on: {project}.\n\n"
                    f"The estimated budget required is {budget}. I am seeking funding to bring this vision to life."
                )
                st.text(proposal_text)

                pdf_bytes = generate_proposal_pdf(proposal_text)
                base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
                pdf_display = (
                    f'<a href="data:application/octet-stream;base64,{base64_pdf}" download="proposal.pdf">'
                    "📄 Download Proposal as PDF</a>"
                )
                st.markdown(pdf_display, unsafe_allow_html=True)

    # Contact form
    st.subheader("📬 Contact Us")
    with st.form("contact_form"):
        contact_name = st.text_input("Your Name", key="contact_name")
        contact_email = st.text_input("Your Email")
        contact_message = st.text_area("Your Message")
        contact_submitted = st.form_submit_button("Send Message")

        if contact_submitted:
            st.success("Thank you for reaching out! We'll get back to you soon.")

if __name__ == "__main__":
    main()