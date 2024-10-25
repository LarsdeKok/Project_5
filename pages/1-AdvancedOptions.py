import streamlit as st
import pandas as pd
import math as m
from time import sleep

from ToolLars import aantal_bussen

st.set_page_config(page_title="Advanced Options", page_icon="📈")

def generate_values(aantallen):
    inputfields = {}
    for i in aantallen:
        inputfields[int(i)] = st.number_input(f"Insert the SOH for bus {i}.", step=1, format="%d", min_value=10, max_value=100, value=90)
    return pd.DataFrame.from_dict(inputfields, orient="index")

def mainFunction():
    st.markdown("# Advanced Options")
    Dienstregeling = st.session_state["Dienstregeling"]
    afstandsmatrix = st.session_state["Afstandsmatrix"]
    omloop = st.session_state["Omloop"]

    aantallen = aantal_bussen(omloop)
    with st.form("SOH"):
        with st.container(height=350):
            st.session_state["SOHs"] = generate_values(aantallen)
        with st.container(height=(115)):
            st.session_state["Minimal_battery"] = st.slider("Choose the minimum battery percentage:", 0.0, 30.0, 10.0)
        with st.container(height=(115)): 
            st.session_state["Startday_battery"] = st.slider("Choose the battery percentage at the start of the day:", 70.0, 100.0, 90.0)
        with st.container(height=(115)):
            st.session_state["verbruik_rijdend"] = st.slider("Choose the driving battery usage (kW/km):", 0.0, 4.0, 1.2)
        with st.container(height=(115)):
            st.session_state["idle_usage"] = st.slider("Choose the idle battery usage (kW):", 0.0, 1.0, 0.1)
        with st.container(height=(115)):
            st.session_state["Charge_speed"] = st.slider("Choose the charging speed (kWh):", 300, 600, 450)
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.success("Everything adjusted successfuly")
            sleep(2)
            st.switch_page("pages/2-Results.py")
            

if 'FormFilled' not in st.session_state:
    st.write("Please upload your files first.")
else:
    mainFunction()

