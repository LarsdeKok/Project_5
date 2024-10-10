
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as sp
import numpy as np
import streamlit as st

def check_SOC(omloopplanning):
    '''
    
    '''
    SOH = st.session_state["SOHs"]
    capaciteit = 300
    SOC_kolom=[]
    for i in range(1, max(omloopplanning['omloop nummer'])+1):
        df = omloopplanning['omloop nummer'==i]
        max_batterij = SOH[i-1] * capaciteit
        baterij_start = 0.9 * max_batterij # 0.9 omdat wij dervanuit gaan dat de baterij niet verder dan dit oplaad snachts
        min_batterij = 0.1 * max_batterij
        for j in range(len(df)):
            if j == 0:
                SOC=baterij_start
                SOC_kolom.append(SOC)
            else:
                SOC=SOC_kolom[-1]-df['energieverbruik2'][j]
                SOC_kolom.append(SOC)
            


    omloopplanning['SOC']=SOC_kolom
    omloopplanning['min_SOC']=omloopplanning['SOC'<min_batterij]