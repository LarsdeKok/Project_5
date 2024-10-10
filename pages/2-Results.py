import streamlit as st
import pandas as pd
import numpy as np
from ToolLars import duur_activiteiten, oplaadtijd, aanpassingen_op_omloop, Check_dienstregeling, Gantt_chart
from ToolBram import Berekinging_EngergieVerbruik
from SOHFloor import check_SOC

st.set_page_config(page_title="Plotting Demo", page_icon="📈")

def mainFunction():
    omloop = st.session_state["Omloop"]
    Soh = st.session_state["SOHs"]
    Dienstregeling = st.session_state["Dienstregeling"]
    afstandsmatrix = st.session_state["Afstandsmatrix"]
    st.markdown("# Plotting Demo")
    st.sidebar.header("Plotting Demo222222")
    omloop = aanpassingen_op_omloop(omloop,Soh)
    Check_dienstregeling(Dienstregeling, omloop)
    oplaadtijd(omloop)
    Berekinging_EngergieVerbruik(omloop, afstandsmatrix)
    check_SOC(omloop, st.session_state["SOHs"])
    Gantt_chart(omloop)
    st.write(omloop)

    if st.button("Export all used data to Excel"):
        st.write("Yippie")
        #Export functie aanroepen
    ## Hier volgende functies achter plakken


if 'FormFilled' not in st.session_state:
    st.write("Please upload your files first.")
else:
    mainFunction()



