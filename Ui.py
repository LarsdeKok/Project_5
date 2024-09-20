import streamlit as st
import pandas as pd
import numpy as np

st.title('test2')

st.write('test')

dienstregeling = st.file_uploader('Dienstregeling')
omloop = st.file_uploader('Omloopplanning')

def filesUploaded():
    df1=pd.read_excel(dienstregeling)
    st.write(df1)

if st.button("Submit"):
    if dienstregeling is not None and omloop is not None:
        st.write("Why hello there")
        filesUploaded()
    else:
        st.write("Please add the files first.")

from ToolLars import aantal_bussen
aantallen = aantal_bussen(omloop)
