import pandas as pd
import streamlit as st
        
def check_SOC(omloopplanning, SOH):
    capaciteit = 300
    SOC_kolom = []
    omloopplanning['min_batterij'] = 0

    for i in range(1, max(omloopplanning['omloop nummer']) + 1):
        df = omloopplanning[omloopplanning['omloop nummer'] == i]
        
        if isinstance(SOH, list):
            max_batterij = float(SOH[i - 1]) / 100 * capaciteit
        elif isinstance(SOH, pd.DataFrame):
            max_batterij = float(SOH.iloc[i - 1]) / 100 * capaciteit
        else:
            raise Exception("Something went wrong with the SOH")

        batterij_start = 0.9 * max_batterij  # Assume battery is charged to 90%
        min_batterij = 0.1 * max_batterij  # Minimum allowed battery level
        omloopplanning.loc[omloopplanning['omloop nummer'] == i, 'min_batterij'] = min_batterij

        # Loop over each row in df
        for idx, row in df.iterrows():
            if idx == df.index[0]:  # First row of this omloop
                SOC = batterij_start
            else:
                SOC = SOC_kolom[-1] - row['energieverbruik2']  # Calculate SOC after energy consumption

            SOC_kolom.append(SOC)
        
    omloopplanning['SOC'] = SOC_kolom
    omloopplanning['Below_min_SOC'] = omloopplanning['SOC'] < omloopplanning['min_batterij']
    soc_tolow = omloopplanning[["rijnummer", "startlocatie", "starttijd", "eindtijd", "omloop nummer", "min_batterij","SOC"]][omloopplanning["Below_min_SOC"]==True]
    if len(soc_tolow) > 0:
        st.write("In the following rows the bus gets below the minimum battery level")
        st.write(soc_tolow)
    else:
        st.write("✓) All busses stay above the minimum battery level")



    