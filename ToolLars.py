## if __name__== __main__ voor tests
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as sp
import numpy as np
import streamlit as st
import plotly.express as px


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
    rows = []
    for i in range(len(omloop) - 1):
        rows.append(omloop.iloc[i])
        if omloop.iloc[i]['eindtijd'] != omloop.iloc[i + 1]['starttijd']:
            gap_row = pd.Series({
                'eindtijd': omloop.iloc[i+1]["starttijd"], 
                'starttijd': omloop.iloc[i]["eindtijd"],
                'activiteit': "idle",
                'eindtijd datum': omloop.iloc[i+1]["starttijd datum"], 
                'starttijd datum': omloop.iloc[i]["eindtijd datum"],
                'omloop nummer' : omloop.iloc[i]["omloop nummer"],
                "energieverbruik": 0.01
            })
            rows.append(gap_row)
    rows.append(omloop.iloc[-1])
    omloop = pd.concat([pd.DataFrame([row]) for row in rows], ignore_index=True)
    
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
        st.write(f"The following charge times are to short.")
        st.write(tekortopladen[["starttijd","eindtijd","activiteit","omloop nummer"]])
    else:
        st.write("✓) Each bus is charged for at least 15 minutes.")


def Check_dienstregeling(connexxion_df, omloopplanning_df):
    connexxion_df['vertrektijd'] = pd.to_datetime(connexxion_df['vertrektijd'], format='%H:%M').dt.time
    omloopplanning_df['starttijd'] = pd.to_datetime(omloopplanning_df['starttijd'], format='%H:%M:%S').dt.time
    omloopplanning_df['eindtijd'] = pd.to_datetime(omloopplanning_df['eindtijd'], format='%H:%M:%S').dt.time
    
    uncovered_rides = []
    
    for idx, ride in connexxion_df.iterrows():
        ride_covered = False
        
        matching_omloop = omloopplanning_df[
            (omloopplanning_df['buslijn'] == ride['buslijn']) & 
            (omloopplanning_df['startlocatie'] == ride['startlocatie']) & 
            (omloopplanning_df['eindlocatie'] == ride['eindlocatie'])
        ]

        for _, omloop in matching_omloop.iterrows():
            if omloop['starttijd'] == ride['vertrektijd']:
                ride_covered = True
                break
        
        if not ride_covered:
            uncovered_rides.append(ride)
    
    if uncovered_rides:
        st.write("The following rides won't be driven, given your bus planning.")
        st.write(pd.DataFrame(uncovered_rides))
    else:
        st.write("✓) All bus rides will be driven on time, given your bus planning.")


def Gantt_chart(omloop):
    omloop = omloop.drop(omloop[omloop["diff"] > pd.Timedelta(hours = 1.5)].index)
    omloop = omloop.drop(omloop[omloop["diff"] >= pd.Timedelta(days = 1)].index)
    omloop = omloop.drop(omloop[omloop["diff2"] < 0].index)
    omloop['starttijd datum'] = pd.to_datetime(omloop['starttijd datum'])
    omloop['eindtijd datum'] = pd.to_datetime(omloop['eindtijd datum'])

    fig = px.timeline(omloop, x_start="starttijd datum", x_end="eindtijd datum", y="omloop nummer", color="activiteit")
    fig.update_yaxes(tickmode='linear', tick0=1, dtick=1, autorange="reversed", showgrid=True, gridcolor='lightgray', gridwidth=1)
    fig.update_xaxes(tickformat="%H:%M", showgrid=True, gridcolor="lightgray", gridwidth = 1)
    fig.update_layout(
    title=dict(text="Gantt chart of the given bus planning", font=dict(size=30))
    )
    fig.update_layout(legend=dict(
    yanchor="bottom",
    y=0.01,
    xanchor="right",
    x=0.999
))
    return st.plotly_chart(fig)