
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as sp
import numpy as np
import streamlit as st


omloopplanning = pd.read_excel("omloopplanning.xlsx")

SOH = st.session_state["SOHs"]

# Functie om de SOC te berekenen op basis van de SOH en te controleren of deze minstens 10% is
def check_SOC(SOH):
   
    max_SOC = 0.9 * SOH  # De bus wordt tot 90% van de SOH opgeladen
    beschikbare_SOC = max_SOC - 10  # Houd rekening met de veiligheidsmarge van 10%

    # ik weet niet zeker of hier 0 of 10 moet staan. (aangezien je de veiligheidsmarge al deraf haalt.)
    if beschikbare_SOC >= 0:
        return True
    else:
        return False

# Testen
check_SOC(85)  # resultaat True of False 
