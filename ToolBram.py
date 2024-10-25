import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as sp
import numpy as np
import streamlit as st

def omloopplanning_buslijn(omloopplanning, my_bar, bar_increment):
    '''
    Replaces the empty cells in 'buslijn' with the corresponding 'activiteit'
    '''
    omloopplanning['buslijn'] = omloopplanning['buslijn'].fillna('##')
    for i in range(len(omloopplanning)):
        if omloopplanning.loc[i, 'activiteit']=='materiaal rit':
            omloopplanning.loc[i, 'buslijn']=omloopplanning['buslijn'][i].replace('##','materiaalrit')
        if omloopplanning.loc[i, 'activiteit']=='opladen':
            omloopplanning.loc[i, 'buslijn']=omloopplanning['buslijn'][i].replace('##','opladen')
        if omloopplanning.loc[i, 'activiteit']=='idle':
            omloopplanning.loc[i, 'buslijn']=omloopplanning['buslijn'][i].replace('##','idle')
        my_bar.progress((i/100)*bar_increment, f"Recalculating distances and energy-usage: {100*((i/100)*bar_increment):.1f}%")
    omloopplanning['buslijn'] = omloopplanning['buslijn'].apply(lambda x: int(x) if isinstance(x, float) else x)

def afstandcode_maken(omloopplanning, my_bar, bar_increment, current_progress):
    '''
    Creates a new column called 'afstandcode' which corresponds to the afstandcode in the dictionary
    '''
    omloopplanning['afstandcode']=''
    for i in range(len(omloopplanning)):
        omloopplanning.loc[i, 'afstandcode']=f"{omloopplanning['startlocatie'][i]}{omloopplanning['eindlocatie'][i]}{omloopplanning['buslijn'][i]}"
        my_bar.progress(current_progress+(i/100)*bar_increment, f'Recalculating distances and energy-usage: {100*(current_progress+(i/100)*bar_increment):.1f}%')

def energieverbruik_berekenen(omloopplanning, afstand:dict, rijdend_verbruik:float, stilstaand_verbruik:float, laadsnelheid:float, my_bar, bar_increment:float, current_progress:float):
    '''
    Creates a new column called 'energieverbruik2' which contains the newly calculated energy usage.
    rijdend_verbruik is in kW/km
    stilstaand_verbruik is constant
    laadsnelheid is in kW/h
    '''
    omloopplanning['energieverbruik2']=''
    omloopplanning['diff2']=omloopplanning['diff'].dt.total_seconds() / 60
    for i in range(len(omloopplanning)):
        if 'idle' in omloopplanning['afstandcode'][i]:
            omloopplanning.loc[i, 'energieverbruik2']=stilstaand_verbruik
        elif 'opladen' in omloopplanning['afstandcode'][i]:
            omloopplanning.loc[i, 'energieverbruik2']=(omloopplanning['diff2'][i]*laadsnelheid*-1)/60
        else:
            omloopplanning.loc[i, 'energieverbruik2']=(afstand[omloopplanning['afstandcode'][i]]/1000)*rijdend_verbruik
        my_bar.progress(current_progress+(i/100)*bar_increment, f'Recalculating distances and energy-usage: {100*(current_progress+(i/100)*bar_increment):.1f}%')

def Berekinging_EngergieVerbruik(omloopplanning,afstandsmatrix, driving_use, idle_use, Chargespeed):
    # Progress bar
    st.markdown(
        """
        <style>
        .stProgress > div > div > div > div {
            background-color: green;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    my_bar=st.progress(0, "Recalculating distances and energy-usage.")
    total=(3*len(omloopplanning)+len(afstandsmatrix))
    bar_increment=100/total
    
    # Defining parameters
    rijdend_verbruik=driving_use # kW per kilometer
    stilstaand_verbruik=idle_use # Altijd (onafhankelijk van tijd)
    laadsnelheid=Chargespeed # kW per uur

    # Fill blanks in 'Buslijn' with 'materiaalrit'
    afstandsmatrix = afstandsmatrix.fillna('materiaalrit')

    # Convert floats to integers and leave strings as is
    afstandsmatrix['buslijn'] = afstandsmatrix['buslijn'].apply(lambda x: int(x) if isinstance(x, float) else x)

    # In omloopplanning, make the column 'buslijn' more workable
    omloopplanning_buslijn(omloopplanning, my_bar, bar_increment)

    # Create dictionary with distances
    afstand={}
    for i in range(len(afstandsmatrix)):
        afstand[f"{afstandsmatrix['startlocatie'][i]}{afstandsmatrix['eindlocatie'][i]}{afstandsmatrix['buslijn'][i]}"]=afstandsmatrix['afstand in meters'][i]
    current_progress=((len(omloopplanning)+len(afstandsmatrix))/100)*bar_increment
    my_bar.progress(current_progress, f"Recalculating distances and energy-usage: {current_progress:.1f}")
    # Add column afstandcode
    afstandcode_maken(omloopplanning, my_bar, bar_increment, current_progress)
    current_progress=((2*len(omloopplanning)+len(afstandsmatrix))/100)*bar_increment
    
    # Add column energieverbruik2
    energieverbruik_berekenen(omloopplanning, afstand, rijdend_verbruik, stilstaand_verbruik, laadsnelheid, my_bar, bar_increment, current_progress)
    my_bar.empty()
    st.success('✓) Calculations complete.')