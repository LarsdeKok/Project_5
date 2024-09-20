import streamlit as st
import pandas as pd
import numpy as np

from ToolLars import aantal_bussen


st.set_page_config(
    page_title="Planning Checker",
    page_icon="👋",
)
# st.sidebar.title("Plotting Demo")

# st.sidebar.success("Select a demo above.")


st.title('test2')

st.write('test')



dienstregeling = st.file_uploader('Dienstregeling', type=['xlsx'],accept_multiple_files=False)
omloop = st.file_uploader('Omloopplanning', type=['xlsx'],accept_multiple_files=False)

inputfields = []

def filesUploaded():
    dfomloop=pd.read_excel(omloop)
    dfdienst=pd.read_excel(dienstregeling)

    st.session_state['Omloop'] = dfomloop
    st.session_state['Dienstregeling'] = dfdienst

    aantallen = aantal_bussen(dfomloop)
    generate_values(aantallen)

def generate_values(aantallen):
    for i in aantallen:
        inputfields.append(st.number_input(f"Insert the SOH for bus {i}.", step=1, format="%d", min_value=10, max_value=100))
    if st.button("Submit"):
        st.write('check voor values')
        doTheChecks()


def doTheChecks():
    st.session_state['SOHs'] = inputfields
    st.switch_page("pages/Results.py")
    

with st.popover("Submit files"):
    if dienstregeling is not None and omloop is not None:
        filesUploaded()
    else:
        st.write("Please add the files first.")




# for i in aantallen:
#     inputfields.append(st.number_input(f"Insert the SOH for bus {i}."))
