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
    omloop['starttijd'] = pd.to_datetime(omloop['starttijd'], format='%H:%M:%S').dt.time
    omloop['eindtijd'] = pd.to_datetime(omloop['eindtijd'], format='%H:%M:%S').dt.time
    return omloop

def oplaadtijd(omloop):
    oplaadmomenten = omloop[omloop.iloc[:,5].str.contains("opladen")]
    tekortopladen = oplaadmomenten[oplaadmomenten['diff'] < pd.Timedelta(minutes=15)]
    if len(tekortopladen.index) > 0:
        st.write(tekortopladen)
        st.write(f"The following charge times are to short.")
    else:
        st.write("✓) Each bus is charged for at least 15 minutes")

def Check_dienstregeling(connexxion_df, omloopplanning_df):
    """
    Function to check if all rides in the Connexxion data are covered by the omloopplanning
    and return a dataframe of uncovered rides.
    
    Args:
    connexxion_df (pd.DataFrame): Connexxion rides data.
    omloopplanning_df (pd.DataFrame): Omloopplanning data.
    
    Returns:
    pd.DataFrame: DataFrame of rides that are not covered in the omloopplanning.
    """
    # Convert time columns to datetime for accurate comparisons
    connexxion_df['vertrektijd'] = pd.to_datetime(connexxion_df['vertrektijd'], format='%H:%M').dt.time
    omloopplanning_df['starttijd'] = pd.to_datetime(omloopplanning_df['starttijd'], format='%H:%M:%S').dt.time
    omloopplanning_df['eindtijd'] = pd.to_datetime(omloopplanning_df['eindtijd'], format='%H:%M:%S').dt.time
    
    uncovered_rides = []
    
    # Iterate over each ride in the Connexxion data
    for idx, ride in connexxion_df.iterrows():
        ride_covered = False
        
        # Filter omloopplanning for matching bus line, start, and end locations
        matching_omloop = omloopplanning_df[
            (omloopplanning_df['buslijn'] == ride['buslijn']) & 
            (omloopplanning_df['startlocatie'] == ride['startlocatie']) & 
            (omloopplanning_df['eindlocatie'] == ride['eindlocatie'])
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
        st.write("The following rides won't be driven, given your bus planning")
        st.write(pd.DataFrame(uncovered_rides))
    else:
        st.write("✓) All bus rides will be driven on time, given your bus planning")