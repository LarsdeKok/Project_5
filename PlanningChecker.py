import streamlit as st
import pandas as pd
import numpy as np

from ToolLars import aantal_bussen

st.set_page_config(
    page_title="Planning Checker",
    page_icon="👋",
)
st.title('Planning checker')
st.write('Made by: Group 8')

def filesUploaded(dienstregeling, omloop):
    dfomloop=pd.read_excel(omloop)
    dfdienst=pd.read_excel(dienstregeling)

    st.session_state['Omloop'] = dfomloop
    st.session_state['Dienstregeling'] = dfdienst

    aantallen = aantal_bussen(dfomloop)
    generate_values(aantallen)

def generate_values(aantallen):
    inputfields = []
    for i in aantallen:
        inputfields.append(st.number_input(f"Insert the SOH for bus {i}.", step=1, format="%d", min_value=10, max_value=100))
    if st.button("Submit"):
        st.write('check voor values')
        doTheChecks(inputfields)

def doTheChecks(inputfields):
    st.session_state['SOHs'] = inputfields
    st.session_state['FormFilled'] = True

    st.switch_page("pages/Results.py")

if 'FormFilled' not in st.session_state:


    dienstregeling = st.file_uploader('Dienstregeling', type=['xlsx'],accept_multiple_files=False)
    omloop = st.file_uploader('Omloopplanning', type=['xlsx'],accept_multiple_files=False)

    with st.popover("Submit files"):
        if dienstregeling is not None and omloop is not None:
            filesUploaded(dienstregeling, omloop)
        else:
            st.write("Please add the files first.")
else:
    st.write('Do you want to reset your data?')
    if st.button("Reset"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.switch_page("PlanningChecker.py")





# for i in aantallen:
#     inputfields.append(st.number_input(f"Insert the SOH for bus {i}."))