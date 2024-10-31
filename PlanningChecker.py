import streamlit as st
import pandas as pd
import numpy as np

from ToolLars import aantal_bussen, format_check

st.set_page_config(
    page_title="Planning Checker",
    page_icon="👋",
)
st.title('Planning checker')
st.write('Made by: Group 8')

def filesUploaded(dienstregeling, omloop):
    """
    Leest alle geuploade bestanden, zet ze om naar een Pands DataFrame en checkt
    het verschillende omlopen in de gegeven planning.
    """
    dfomloop=pd.read_excel(omloop)
    dfdienst=pd.read_excel(dienstregeling)
    dfafstand = pd.read_excel(dienstregeling, "Afstandsmatrix")

    st.session_state['Omloop'] = dfomloop
    st.session_state['Dienstregeling'] = dfdienst
    st.session_state["Afstandsmatrix"] = dfafstand

    aantallen = aantal_bussen(dfomloop)
    generate_values(aantallen)

def generate_values(aantallen):
    """
    Genereerd een dataframe voor iedere unieke bus een SOH van 90 indien de advanced 
    opties worden gebruikt. 

    Returns
    -------
    Inputfields: Pandas DataFrame met als index omloop nummer/index en een SOH waarde 
    van 90%
    """

    inputfields = {}
    for i in aantallen:
        inputfields[int(i)] = 90
    doTheChecks(pd.DataFrame.from_dict(inputfields, orient="index"))

def doTheChecks(inputfields):
    """
    Stelt indien geen advanced opties gebruikt worden standaardwaarden in voor alle nodige 
    session state variabelen en verwijst de gebruiker door naar de resultaten pagina
    """

    st.session_state['SOHs'] = inputfields
    st.session_state['FormFilled'] = True
    st.session_state["Minimal_battery"] = 10
    st.session_state["Startday_battery"] = 90
    st.session_state["verbruik_rijdend"] = 1.2  
    st.session_state["idle_usage"] = 0.1
    st.session_state["Charge_speed"] = 450

    st.switch_page("pages/2-Results.py")



# """
# Doorloopt alle nodige stappen op de startpagina en indien alles klopt zend de gebruiker door
# naar de results of AdvancedOptions pagina.
# """

if 'FormFilled' not in st.session_state:
    # File upload section
    dienstregeling = st.file_uploader('Time table', type=['xlsx'], accept_multiple_files=False)
    omloop = st.file_uploader('Bus planning', type=['xlsx'], accept_multiple_files=False)
    if omloop is not None:
        format_check(pd.read_excel(omloop))
    if dienstregeling is not None and omloop is not None:
        # Ask if the user wants to use advanced options
        use_advanced = st.checkbox("Use advanced options")
        st.session_state["use_advanced"] = use_advanced
        # Submit button for file uploads
        if st.button("Submit files"):
            if use_advanced:
                st.session_state['FormFilled'] = True
                dfomloop=pd.read_excel(omloop)
                dfdienst=pd.read_excel(dienstregeling)
                dfafstand = pd.read_excel(dienstregeling, "Afstandsmatrix")

                st.session_state['Omloop'] = dfomloop
                st.session_state['Dienstregeling'] = dfdienst
                st.session_state["Afstandsmatrix"] = dfafstand

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
