import streamlit as st
import pandas as pd
import math as m

from ToolLars import aantal_bussen

def generate_values(aantallen):
    inputfields = {}
    for i in aantallen:
        inputfields[int(i)] = st.number_input(f"Insert the SOH for bus {i}.", step=1, format="%d", min_value=10, max_value=100, value=90)

def mainFunction():
    omloop = st.session_state["Omloop"]
    Soh = st.session_state["SOHs"]
    Dienstregeling = st.session_state["Dienstregeling"]
    afstandsmatrix = st.session_state["Afstandsmatrix"]
    aantallen = aantal_bussen(omloop)
    generate_values(aantallen)





# soh					Int inputfield(s)
# min baterijlevel			Int inputfield
# baterijlevel start			Int inputfield
# tempo v.d. ritten (rijdend verbruik)	slider
# laadsnelheid				Int inputfield
# stilstaand verbruik			slider