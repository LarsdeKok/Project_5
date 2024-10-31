import streamlit as st
import pandas as pd
import numpy as np
from streamlit_pdf_viewer import pdf_viewer

st.set_page_config(page_title="User manual", page_icon="📖")

st.title('User manual')


file_path = "Project_5_Manual.pdf"

# Open het PDF-bestand en lees het in binair formaat
with open(file_path, "rb") as file:
    file_data = file.read()

st.write("## PDF Preview")
st.download_button(
    label="Download Project 5 Manual",
    data=file_data,
    file_name="Project_5_Manual.pdf",
    mime="application/pdf"
)
with st.container(height=500):
    pdf_viewer(file_path)