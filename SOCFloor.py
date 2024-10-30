import pandas as pd
import streamlit as st

def intervals(df:pd.DataFrame)->pd.DataFrame:
    '''
    Takes a DataFrame from the omloopplanning and outputs a new DataFrame containing the omloop nummers and the
    intervals in which they get below their minimum SOC value.
    '''
    new_interval=True
    omloop=[]
    starttijd=[]
    eindtijd=[]
    for i in range(len(df)):
        if new_interval==True:
            omloop.append(df['omloop nummer'].iloc[i])
            starttijd.append(df['starttijd'].iloc[i])
            new_interval=False
        elif i not in [0, len(df)-1] and df['starttijd'].iloc[i+1]!=df['eindtijd'].iloc[i]:
            eindtijd.append(df['eindtijd'].iloc[i])
            new_interval=True
        elif i==len(df)-1:
            eindtijd.append(df['eindtijd'].iloc[i])
    out=pd.DataFrame()
    out['omloop nummer']=omloop
    out['starttijd']=starttijd
    out['eindtijd']=eindtijd
    return out

        
def check_SOC(omloopplanning, SOH, minbat, startbat):
    '''
    Checks if the SOC of all busses gets below the minimal value
    and returns a DataFrame containing the rows in which a bus has an unallowed SOC value
    '''
    capaciteit = 300
    SOC_kolom = []
    omloopplanning['min_batterij (kW)'] = 0

    for i in range(1, max(omloopplanning['omloop nummer']) + 1):
        df = omloopplanning[omloopplanning['omloop nummer'] == i]
        
        if isinstance(SOH, list):
            max_batterij = float(SOH[i - 1]) / 100 * capaciteit
        elif isinstance(SOH, pd.DataFrame):
            max_batterij = float(SOH.iloc[i - 1]) / 100 * capaciteit
        else:
            raise Exception("Something went wrong with the SOH")

        batterij_start = (startbat/100) * max_batterij  # Battery level after charging
        min_batterij = (minbat/100) * max_batterij  # Minimum allowed battery level
        omloopplanning.loc[omloopplanning['omloop nummer'] == i, 'min_batterij (kW)'] = min_batterij

        # Loop over each row in df
        for idx, row in df.iterrows():
            if idx == df.index[0]:  # First row of this omloop
                SOC = batterij_start
            else:
                SOC = SOC_kolom[-1] - row['energieverbruik2']  # Calculate SOC after energy consumption

            SOC_kolom.append(SOC)
        
    omloopplanning['SOC (kW)'] = SOC_kolom
    omloopplanning['Below_min_SOC'] = omloopplanning['SOC (kW)'] < omloopplanning['min_batterij (kW)']
    soc_tolow = omloopplanning[["rijnummer", "startlocatie", "starttijd", "eindtijd", "omloop nummer", "min_batterij (kW)","SOC (kW)"]][omloopplanning["Below_min_SOC"]==True]
    if len(soc_tolow) > 0:
        output=intervals(soc_tolow)
        expander=st.expander(f"There are {len(output)} intervals where a bus is below the minimum SOC value")
        #expander.write("The following busses get below their minimum battery level")
        expander.write(output)
        #st.write(soc_tolow)
        #st.write("In the following rows the bus gets below the minimum battery level")
    else:
        st.success("✓) All busses stay above the minimum battery level")