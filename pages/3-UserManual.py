import streamlit as st
import pandas as pd
import numpy as np
from streamlit_pdf_viewer import pdf_viewer
import base64

st.set_page_config(page_title="User manual", page_icon="📖")

st.title('User manual')


file_path = "Project_5_Manual.pdf"

uploaded_file = st.file_uploader(file_path, type="pdf")

def displayPDF(file):
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000" type="application/pdf"></iframe>'
    st.components.v1.html(pdf_display, height=1000)


# def displayPDF(file):
#     with open(file, "rb") as f:
#         base64_pdf = base64.b64encode(f.read()).decode('utf-8')
#     pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000" type="application/pdf">'
#     st.markdown(pdf_display, unsafe_allow_html=True)

if uploaded_file is not None:
    displayPDF(uploaded_file)