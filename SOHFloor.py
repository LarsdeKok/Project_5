import pandas as pd
import streamlit as st
        
def is_a_number(a):
    num_value = pd.to_numeric(a, errors='coerce')
    return pd.isna(num_value)

def check_SOC(omloopplanning, SOH):
    '''
    
    '''
    capaciteit = 300
    SOC_kolom=[]
    omloopplanning['min_batterij']=0
    for i in range(1, max(omloopplanning['omloop nummer'])+1):
        df = omloopplanning[omloopplanning['omloop nummer']==i]
        if isinstance(SOH, list):
            max_batterij = float(SOH[i-1])/100 * capaciteit
        elif isinstance(SOH, pd.DataFrame):
            max_batterij = float(SOH.iloc[i-1])/100 * capaciteit
        else:
            st.error("Something went wrong with the SOH")
                    
        batterij_start = 0.9 * max_batterij # 0.9 omdat wij dervanuit gaan dat de baterij niet verder dan dit oplaad snachts
        min_batterij = 0.1 * max_batterij
        omloopplanning.loc[omloopplanning['omloop nummer'] == i, 'min_batterij'] = min_batterij
        
        for j in range(min(df['rijnummer']), max(df['rijnummer'])+1):
            if j == min(df['rijnummer']):
                SOC=batterij_start
                SOC_kolom.append(SOC)
            else:
                SOC=SOC_kolom[-1]-(float(df['energieverbruik2'][j]))
                SOC_kolom.append(SOC)
            if is_a_number(omloopplanning['min_batterij'][j]):
                omloopplanning['min_batterij'][j]=omloopplanning['min_batterij'][j-1]
        

    omloopplanning['SOC']=SOC_kolom
    omloopplanning['Below_min_SOC']=omloopplanning['SOC']<omloopplanning['min_batterij']
    st.write(omloopplanning[omloopplanning['Below_min_SOC']==True])