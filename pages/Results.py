import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Plotting Demo", page_icon="📈")

def mainFunction():
    omloop = st.session_state["Omloop"]
    Soh = st.session_state["SOHs"]

    st.markdown("# Plotting Demo")
    st.sidebar.header("Plotting Demo222222")
    omloop = omloop.merge(Soh ,left_on = omloop[omloop.columns[len(omloop.columns)-1]], right_on = Soh.index)
    omloop = omloop.drop(omloop.columns[[0, 1, -1]], axis=1)
    st.write(omloop)

if 'FormFilled' not in st.session_state:
    st.write("Please enter data first.")
else:
    mainFunction()



