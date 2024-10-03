import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as sp
import numpy as np
import streamlit as st


omloopplanning = pd.read_excel("omloopplanning.xlsx")

SOH = st.session_state["SOHs"]

