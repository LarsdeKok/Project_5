import streamlit as st
import pandas as pd
import numpy as np
from ToolLars import duur_activiteiten, oplaadtijd, aanpassingen_op_omloop
#from ToolBram import [Naam functie]

st.set_page_config(page_title="Plotting Demo", page_icon="📈")

def mainFunction():
    omloop = st.session_state["Omloop"]
    Soh = st.session_state["SOHs"]
    st.markdown("# Plotting Demo")
    st.sidebar.header("Plotting Demo222222")
    omloop = aanpassingen_op_omloop(omloop,Soh)
    oplaadtijd(omloop)
    ## Hier volgende functies achter plakken
    st.write(omloop)


if 'FormFilled' not in st.session_state:
    st.write("Please enter data first.")
else:
    mainFunction()



