import streamlit as st
import logging
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import json
import requests
from bs4 import BeautifulSoup
import os
import platform
from PIL import Image
import io
from datetime import datetime, timedelta
from unittest.mock import patch

# Setup logging for debugging (logs to logs.txt)
logging.basicConfig(
    filename="logs.txt",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Verify Windows 10
if platform.system() != "Windows" or platform.release() != "10":
    st.warning("This app is optimized for Windows 10. Some features may not work on other systems.")

# Function to generate a detailed grant proposal with letterhead and logo
def generate_proposal(project_data, logo_path=None):
    try:
        doc = Document()
        section = doc.sections[0]
        header = section.header
        header_para = header.paragraphs[0]
        header_para.text = "Ubuntu Dance and Theatre Arts\nTafelsig, Mitchells Plain, Western Cape, South Africa\nEmail: info@ubuntudance.org | Phone: +27 21 123 4567"
        header_para.style.font.size = Pt(10)
        header_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        if logo_path and os.path.exists(logo_path):
            try:
                doc.add_picture(logo_path, width=Inches(1.0))
            except Exception as e:
                st.error(f"Failed to add logo: {e}. Using placeholder.")
                logging.warning(f"Logo load failed: {e}")
                doc.add_paragraph("[Ubuntu Dance and Theatre Arts Logo]", style="Heading 1").alignment = WD_ALIGN_PARAGRAPH.CENTER
        else:
            doc.add_paragraph("[Ubuntu Dance and Theatre Arts Logo]", style="Heading 1").alignment = WD_ALIGN_PARAGRAPH.CENTER

        doc.add_heading(f"{project_data['title']} Grant Proposal", 0)
        doc.add_paragraph(f"Prepared for: Potential Funders\nDate: {datetime.now().strftime('%B %d, %Y')}")
        doc.add_page_break()
        doc.add_heading("Executive Summary", level=1)
        doc.add_paragraph(project_data['overview'])
        doc.add_heading("Objectives", level=1)
        for obj in project_data['objectives']:
            doc.add_paragraph(f"- {obj}", style="List Bullet")
        doc.add_heading("Community Impact", level=1)
        doc.add_paragraph(project_data['impact'])
        doc.add_heading("Budget", level=1)
        doc.add_paragraph(f"Total Budget: {project_data['budget_total']} ZAR")
        for item, amount in project_data['budget_items'].items():
            doc.add_paragraph(f"{item}: {amount} ZAR")
        doc.add_heading("Timeline", level=1)
        doc.add_paragraph(project_data['timeline'])
        doc.add_heading("Appendices", level=1)
        doc.add_heading("Demographics", level=2)
        doc.add_paragraph(project_data['demographics']['description'])
        doc.add_heading("Team", level=2)
        doc.add_paragraph("Project Lead: [Your Name]\nArtistic Director: [Director Name]\nCommunity Liaison: [Liaison Name]")
        filename = os.path.join(os.getcwd(), f"{project_data['title'].replace(' ', '_')}_Proposal.docx")
        doc.save(filename)
        return filename
    except Exception as e:
        logging.exception("Proposal generation failed")
        st.error(f"Failed to generate proposal: {e}")
        return None

# Function to generate form data
def generate_form_data(project_data):
    try:
        form_data = {
            "project_title": project_data['title'],
            "overview": project_data['overview'],
            "objectives": project_data['objectives'],
            "community_impact": project_data['impact'],
            "budget": {
                "total": project_data['budget_total'],
                "items": project_data['budget_items']
            },
            "timeline": project_data['timeline'],
            "demographics": project_data.get('demographics', {}),
            "organization": "Ubuntu Dance and Theatre Arts",
            "location": "Tafelsig, Mitchells Plain, Western Cape",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return form_data
    except Exception as e:
        logging.exception("Form data generation failed")
        st.error(f"Failed to generate form data: {e}")
        return None

# Function to scrape grant opportunities with timestamp-based cache expiration
def find_grants(keywords, cache_file="grants_cache.json", expiration_hours=24):
    grants = []
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                cached = json.load(f)
                timestamp = datetime.strptime(cached.get("last_updated", "1970-01-01 00:00:00"), "%Y-%m-%d %H:%M:%S")
                if datetime.now() - timestamp < timedelta(hours=expiration_hours):
                    st.info("Using recent cached grant data.")
                    return cached.get("data", [])
        except Exception as e:
            logging.warning(f"Cache load failed: {e}")
            st.error(f"Failed to load cached grants: {e}")

    try:
        urls = ["https://www.nhc.org.za/grants", "https://www.nac.org.za/funding"]
        for url in urls:
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    text = link.get_text().lower()
                    if any(keyword.lower() in text for keyword in keywords):
                        grants.append({
                            "title": link.get_text(),
                            "url": link['href'],
                            "source": url,
                            "summary": text[:50] + "..." if len(text) > 50 else text,
                            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
            except Exception as e:
                logging.warning(f"Error scraping {url}: {e}")
                st.error(f"Error scraping {url}: {e}")
        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump({"last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "data": grants}, f, indent=2)
        except Exception as e:
            logging.error(f"Failed to save cached grants: {e}")
            st.error(f"Failed to save cached grants: {e}")
    except Exception as e:
        logging.exception("Grant scraping failed")
        st.error(f"Grant scraping failed: {e}")
    return grants
