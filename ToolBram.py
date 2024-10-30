import pandas as pd
import scipy.stats as sp
import numpy as np
import streamlit as st

def omloopplanning_buslijn(omloopplanning):
    '''
    Replaces the empty cells in 'buslijn' with the corresponding 'activiteit'
    '''
    omloopplanning['buslijn'] = omloopplanning['buslijn'].fillna('##')
    for i in range(len(omloopplanning)):
        if omloopplanning['activiteit'][i]=='materiaal rit':
            omloopplanning['buslijn'][i]=omloopplanning['buslijn'][i].replace('##','materiaalrit')
        if omloopplanning['activiteit'][i]=='opladen':
            omloopplanning['buslijn'][i]=omloopplanning['buslijn'][i].replace('##','opladen')
        if omloopplanning['activiteit'][i]=='idle':
            omloopplanning['buslijn'][i]=omloopplanning['buslijn'][i].replace('##','idle')
    omloopplanning['buslijn'] = omloopplanning['buslijn'].apply(lambda x: int(x) if isinstance(x, float) else x)

def afstandcode_maken(omloopplanning):
    '''
    Creates a new column called 'afstandcode' which corresponds to the afstandcode in the dictionary
    '''
    omloopplanning['afstandcode']=''
    for i in range(len(omloopplanning)):
        omloopplanning['afstandcode'][i]=f"{omloopplanning['startlocatie'][i]}{omloopplanning['eindlocatie'][i]}{omloopplanning['buslijn'][i]}"

def energieverbruik_berekenen(omloopplanning, afstand:dict, rijdend_verbruik:float, stilstaand_verbruik:float, laadsnelheid:float):
    '''
    Creates a new column called 'energieverbruik2' which contains the newly calculated energy usage.
    rijdend_verbruik is kW/km
    stilstaand_verbruik is constant
    laadsnelheid is kW/h
    '''
    omloopplanning['energieverbruik2']=''
    omloopplanning['diff2']=omloopplanning['diff'].dt.total_seconds() / 60
    for i in range(len(omloopplanning)):
        if 'idle' in omloopplanning['afstandcode'][i]:
            omloopplanning['energieverbruik2'][i]=stilstaand_verbruik
        elif 'opladen' in omloopplanning['afstandcode'][i]:
            omloopplanning['energieverbruik2'][i]=(omloopplanning['diff2'][i]*laadsnelheid*-1)/60
        else:
            omloopplanning['energieverbruik2'][i]=(afstand[omloopplanning['afstandcode'][i]]/1000)*rijdend_verbruik

def Berekinging_EngergieVerbruik(omloopplanning,afstandsmatrix, rijdend_verbruik, stilstaand_verbruik, laadsnelheid):
    # Fill blanks in 'Buslijn' with 'materiaalrit'
    afstandsmatrix = afstandsmatrix.fillna('materiaalrit')

    # Convert floats to integers and leave strings as is
    afstandsmatrix['buslijn'] = afstandsmatrix['buslijn'].apply(lambda x: int(x) if isinstance(x, float) else x)

    # In omloopplanning, make the column 'buslijn' more workable
    omloopplanning_buslijn(omloopplanning)

    # Create dictionary with distances
    afstand={}
    for i in range(len(afstandsmatrix)):
        afstand[f"{afstandsmatrix['startlocatie'][i]}{afstandsmatrix['eindlocatie'][i]}{afstandsmatrix['buslijn'][i]}"]=afstandsmatrix['afstand in meters'][i]

    # Add column afstandcode
    afstandcode_maken(omloopplanning)

    # Add column energieverbruik2
    energieverbruik_berekenen(omloopplanning, afstand, rijdend_verbruik, stilstaand_verbruik, laadsnelheid)