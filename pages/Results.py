import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Plotting Demo", page_icon="📈")

def mainFunction():
    st.markdown("# Plotting Demo")
    st.sidebar.header("Plotting Demo222222")
    st.write(st.session_state['SOHs'])
    st.write(st.session_state['Omloop'])

if 'FormFilled' not in st.session_state:
    st.write("Please enter data first.")
else:
    mainFunction()



