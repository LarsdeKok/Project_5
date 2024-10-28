import streamlit as st
import pandas as pd
import numpy as np
import io

from ToolLars import duur_activiteiten, oplaadtijd, aanpassingen_op_omloop, Check_dienstregeling, Gantt_chart
from ToolBram import Berekinging_EngergieVerbruik
from SOCFloor import check_SOC

st.set_page_config(page_title="Results", page_icon="📈")

def mainFunction():
    minbat = st.session_state["Minimal_battery"]
    startbat = st.session_state["Startday_battery"]
    driving_use = st.session_state["verbruik_rijdend"]
    idle_use = st.session_state["idle_usage"]
    Chargespeed = st.session_state["Charge_speed"]
    omloop = st.session_state["Omloop"]
    Soh = st.session_state["SOHs"]
    Dienstregeling = st.session_state["Dienstregeling"]
    afstandsmatrix = st.session_state["Afstandsmatrix"]

    st.markdown("# Results")
    omloop = aanpassingen_op_omloop(omloop,Soh)
    Check_dienstregeling(Dienstregeling, omloop)
    oplaadtijd(omloop)
    Berekinging_EngergieVerbruik(omloop, afstandsmatrix, driving_use, idle_use, Chargespeed)
    check_SOC(omloop, Soh, minbat, startbat)
    Gantt_chart(omloop)

    buffer = io.BytesIO()
    omloop.to_excel(buffer, index=False, sheet_name='PlanningCheckerData')
    buffer.seek(0)
    st.download_button(
        label="Export all used data to Excel",
        data=buffer,
        file_name="Processed_data.xlsx",
        mime="application/vnd.ms-excel",
        key="Download - excel"
    )

if 'FormFilled' not in st.session_state:
    st.write("Please upload your files first.")
else:
    mainFunction()



