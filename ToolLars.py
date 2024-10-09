## if __name__== __main__ voor tests
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as sp
import numpy as np
import streamlit as st


def aantal_bussen(planning):
    planning = pd.DataFrame(planning)
    bussen = planning[planning.columns[len(planning.columns)-1]].unique()
    return bussen

def duur_activiteiten(omloop):
    omloop[omloop.columns[3]] = pd.to_datetime(omloop.iloc[:,3], format = "%H:%M:%S")
    omloop[omloop.columns[4]] = pd.to_datetime(omloop.iloc[:,4], format = "%H:%M:%S")
    omloop["diff"] = omloop[omloop.columns[4]] - omloop[omloop.columns[3]]
    return omloop

def aanpassingen_op_omloop(omloop, Soh):
    omloop = duur_activiteiten(omloop)
    omloop = omloop.merge(Soh ,left_on = omloop[omloop.columns[len(omloop.columns)-2]], right_on = Soh.index)
    omloop = omloop.drop(omloop.columns[[0]], axis=1)
    omloop.columns.values[0] = "rijnummer"
    omloop.columns.values[len(omloop.columns)-1] = "SOH"
    return omloop

def oplaadtijd(omloop):
    oplaadmomenten = omloop[omloop.iloc[:,5].str.contains("opladen")]
    tekortopladen = oplaadmomenten[oplaadmomenten['diff'] < pd.Timedelta(minutes=15)]
    if len(tekortopladen.index) > 0:
        st.write(tekortopladen)
        st.write(f"De bovenstaande oplaadmomenten zijn te kort.")
    else:
        st.write("✓) Elke bus wordt minimaal 15 minuten opgeladen")

def Check_dienstregeling(dienstregeling, omloop):
    """
    Function to check if all rides in the Connexxion data are covered by the omloopplanning
    and return a dataframe of uncovered rides.
    
    Args:
    dienstregeling (pd.DataFrame): Connexxion rides data.
    omloop (pd.DataFrame): Omloopplanning data.
    
    Returns:
    pd.DataFrame: DataFrame of rides that are not covered in the omloopplanning.
    """    
    uncovered_rides = []
    
    # Iterate over each ride in the Connexxion data
    for idx, ride in dienstregeling.iterrows():
        ride_covered = False
        
        # Filter omloopplanning for matching bus line, start, and end locations
        matching_omloop = omloop[
            (omloop['buslijn'] == ride['buslijn']) & 
            (omloop['startlocatie'] == ride['startlocatie']) & 
            (omloop['eindlocatie'] == ride['eindlocatie'])
        ]
        
        # Check if the vertrektijd of the ride is within the start and end time in omloopplanning
        for _, omloop in matching_omloop.iterrows():
            if omloop['starttijd'] <= ride['vertrektijd'] <= omloop['eindtijd']:
                ride_covered = True
                break
        
        if not ride_covered:
            uncovered_rides.append(ride)
    
    # Return a DataFrame of uncovered rides
    if uncovered_rides:
        return pd.DataFrame(uncovered_rides)
    else:
        return st.write("All rides will be driven using your given bus planning")