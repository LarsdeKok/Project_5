import streamlit as st
import pandas as pd
import numpy as np
from streamlit_pdf_viewer import pdf_viewer
import base64

st.set_page_config(page_title="User manual", page_icon="📖")

st.title('User manual')

with open("Project_5_Manual.pdf", "rb") as file:
    manual_data = file.read()

# Create a download button
st.download_button(
    label="Download PlanningChecker Manual",
    data=manual_data,
    file_name="PlanningChecker_Manual.pdf",
    mime="application/pdf"
)

file_path = "Project_5_Manual.pdf"
file_link = "https://drive.google.com/file/d/189_ccfKl5mTO1tch4SHrO0_C4MbOz73l/view?usp=sharing"

def displayPDF(url):
    pdf_display = f'<iframe src="{url}" width="100%" height="1000" type="application/pdf"></iframe>'
    st.components.v1.html(pdf_display, height=1000)

# Use Google Drive's preview link
displayPDF("https://drive.google.com/file/d/189_ccfKl5mTO1tch4SHrO0_C4MbOz73l/preview")