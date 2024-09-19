import pandas as pd
import scipy.stats as st
import numpy as np

data = pd.read_excel("Connexxion data - 2024-2025.xlsx")
planning = pd.read_excel("omloopplanning.xlsx")


print(data.groupby("buslijn"))
