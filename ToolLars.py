## if __name__== __main__ voor tests
import pandas as pd
import scipy.stats as sp
import numpy as np
import streamlit as st
import plotly.express as px
import datetime


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
    all_rows = []
    for omloop_nummer, group in omloop.groupby('omloop nummer'):
        rows = []
        for i in range(len(group) - 1):
            rows.append(group.iloc[i])
            if group.iloc[i]['eindtijd'] != group.iloc[i + 1]['starttijd']:
                gap_row = pd.Series({
                    'eindtijd': group.iloc[i+1]["starttijd"], 
                    'starttijd': group.iloc[i]["eindtijd"],
                    'activiteit': "idle",
                    'eindtijd datum': group.iloc[i+1]["starttijd datum"], 
                    'starttijd datum': group.iloc[i]["eindtijd datum"],
                    'omloop nummer': group.iloc[i]["omloop nummer"],
                    "energieverbruik": 0.01
                })
                rows.append(gap_row)
        rows.append(group.iloc[-1])
        all_rows.extend(rows)
    omloop = pd.DataFrame(all_rows).reset_index(drop=True)

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
    tekortopladen = oplaadmomenten[oplaadmomenten['diff2'] < pd.Timedelta(minutes=15)]
    if len(tekortopladen) > 0:
        st.error(f"There are {len(tekortopladen)} times a bus is charged too short")
        with st.expander("Click for more information on the charging times mentioned above."):
            st.write("The following charge times need to be longer")
            tekortopladen = tekortopladen[["starttijd", "eindtijd", "activiteit", "omloop nummer", "energieverbruik"]]
            st.write(pd.DataFrame(tekortopladen))
    else:
        st.success("✓) All busses get charged sufficiently long.")
    st.write("")

def parse_time(value):
    if isinstance(value, datetime.time):
        return value
    try:
        return pd.to_datetime(value, format='%H:%M').time()
    except ValueError:
        return pd.to_datetime(value, format='%H:%M:%S').time()

def Check_dienstregeling(connexxion_df, omloopplanning_df):
    # Apply the function to the relevant columns only if they are not already datetime.time
    connexxion_df['vertrektijd'] = connexxion_df['vertrektijd'].apply(parse_time)
    omloopplanning_df['starttijd'] = omloopplanning_df['starttijd'].apply(parse_time)
    omloopplanning_df['eindtijd'] = omloopplanning_df['eindtijd'].apply(parse_time)
    
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

    if len(uncovered_rides) > 1:
        st.error(f"There are {len(uncovered_rides)} rides that won't be driven")
        with st.expander("Click for more information on the rides mentioned above."):
            st.write("The following rides won't be driven given your bus planning")
            st.write(pd.DataFrame(uncovered_rides))
    elif len(uncovered_rides) == 1:
        st.error(f"There is 1 ride that won't be driven")
        with st.expander("Click for more information on the ride mentioned above."):
            st.write("The following ride wont be driven given your bus planning")
            st.write(pd.DataFrame(uncovered_rides))
    else:
        st.success("✓) All rides will be driven given your bus plannning.")
    st.write("")

def Gantt_chart(omloop):
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

def format_check(omloop:pd.DataFrame):
    items = list(omloop.columns)
    true_amount = items == ['Unnamed: 0', 'startlocatie', 'eindlocatie', 'starttijd', 'eindtijd', 
            'activiteit', 'buslijn', 'energieverbruik', 
            'starttijd datum', 'eindtijd datum', 'omloop nummer']
    if true_amount:
        st.success("The uploaded bus planning has the right format")
    if not true_amount:
        st.error("The uploaded bus planning does not have the right format")