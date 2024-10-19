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
    dfafstand = pd.read_excel(dienstregeling, "Afstandsmatrix")

    st.session_state['Omloop'] = dfomloop
    st.session_state['Dienstregeling'] = dfdienst
    st.session_state["Afstandsmatrix"] = dfafstand

    aantallen = aantal_bussen(dfomloop)
    generate_values(aantallen)

def generate_values(aantallen):
    inputfields = {}
    for i in aantallen:
        inputfields[int(i)] = 90
    doTheChecks(pd.DataFrame.from_dict(inputfields, orient="index"))

def doTheChecks(inputfields):
    st.session_state['SOHs'] = inputfields
    st.session_state['FormFilled'] = True

    st.switch_page("pages/2-Results.py")

if 'FormFilled' not in st.session_state:
    # File upload section
    dienstregeling = st.file_uploader('Time table', type=['xlsx'], accept_multiple_files=False)
    omloop = st.file_uploader('Bus planning', type=['xlsx'], accept_multiple_files=False)
    
    if dienstregeling is not None and omloop is not None:
        # Ask if the user wants to use advanced options
        use_advanced = st.checkbox("Use advanced options")

        # Submit button for file uploads
        if st.button("Submit files"):
            if use_advanced:
                # Redirect to the advanced options page
                st.switch_page("pages/1-AdvancedOptions.py")
            else:
                # Continue with normal flow if advanced options are not selected
                filesUploaded(dienstregeling, omloop)
    else:
        st.write("Please add the files first.")
else:
    # Reset data option
    st.write('Do you want to reset your data?')
    if st.button("Reset"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.switch_page("PlanningChecker.py")

# with st.popover("Submit files"): 
#     if dienstregeling is not None and omloop is not None:
#         filesUploaded()
#     else:
#         st.write("Please add the files first.")




# for i in aantallen:
#     inputfields.append(st.number_input(f"Insert the SOH for bus {i}."))
