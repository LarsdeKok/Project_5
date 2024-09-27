import streamlit as st
import pandas as pd
import numpy as np
from ToolLars import duur_activiteiten, oplaadtijd

st.set_page_config(page_title="Plotting Demo", page_icon="📈")

def mainFunction():
    omloop = st.session_state["Omloop"]
    omloop = duur_activiteiten(omloop)
    Soh = st.session_state["SOHs"]
    st.markdown("# Plotting Demo")
    st.sidebar.header("Plotting Demo222222")

    omloop = omloop.merge(Soh ,left_on = omloop[omloop.columns[len(omloop.columns)-2]], right_on = Soh.index)
    omloop = omloop.drop(omloop.columns[[0]], axis=1)
    omloop.columns.values[0] = "rijnummer"
    omloop.columns.values[len(omloop.columns)-1] = "SOH"
    print(omloop)
    
    st.write(omloop)

if 'FormFilled' not in st.session_state:
    st.write("Please enter data first.")
else:
    mainFunction()



