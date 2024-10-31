import streamlit as st
import pandas as pd
import numpy as np
import io

from ToolLars import duur_activiteiten, oplaadtijd, aanpassingen_op_omloop, Check_dienstregeling, Gantt_chart
from ToolBram import Berekinging_EngergieVerbruik
from SOCFloor import check_SOC

st.set_page_config(page_title="Results", page_icon="📈")

def mainFunction():
    """
    Verricht meerdere checks op de busplanning "omloop", deze worden in de volgende stappen verwerkt.

    Verwerkingsstappen
    ------------------
    1. Past de omloopgegevens aan op basis van SOH-waarden.
    2. Berekening van energieverbruik voor de omloop met de ingevoerde rij- en stilstandverbruik en laadsnelheid.
    3. Controleert de omloop tegen de dienstregeling.
    4. Voegt laadtijden toe aan de omloopplanning.
    5. Verifieert SOC (State of Charge) waarden in de omloop tegen minimum- en startwaarden.
    6. Genereert een Gantt-diagram om de omloopplanning te visualiseren.
    
    Export
    ------
    - Converteert start- en eindtijden naar stringformaat 'YYYY-MM-DD'.
    - Exporteert de `omloop` DataFrame naar een Excel-bestand met de naam 'Processed_data.xlsx'.
    - Biedt een downloadknop in Streamlit voor gebruikers om het bestand te downloaden.
    """

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
    Berekinging_EngergieVerbruik(omloop, afstandsmatrix, driving_use, idle_use, Chargespeed)
    Check_dienstregeling(Dienstregeling, omloop)
    oplaadtijd(omloop)
    check_SOC(omloop, Soh, minbat, startbat)
    Gantt_chart(omloop)

    omloop['starttijd datum'] = omloop['starttijd datum'].dt.strftime('%Y-%m-%d')
    omloop['eindtijd datum'] = omloop['eindtijd datum'].dt.strftime('%Y-%m-%d')

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



