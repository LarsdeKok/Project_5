import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st
import numpy as np

# Read excel files
connection_data = pd.read_excel("Connexxion data - 2024-2025.xlsx")
omloopplanning = pd.read_excel("omloopplanning.xlsx")
dienstregeling = pd.read_excel("Connexxion data - 2024-2025.xlsx", sheet_name='Dienstregeling')
afstandsmatrix = pd.read_excel("Connexxion data - 2024-2025.xlsx", sheet_name='Afstandsmatrix')

# Defining parameters
rijdend_verbruik=1.2 # Per kilometer
stilstaand_verbruik=0.01 # Per uur? Minuut??

# Fill blanks in 'Buslijn' with 'materiaalrit'
afstandsmatrix = afstandsmatrix.fillna('materiaalrit')

# Convert floats to integers and leave strings as is
afstandsmatrix['buslijn'] = afstandsmatrix['buslijn'].apply(lambda x: int(x) if isinstance(x, float) else x)

# In omloopplanning, make the column 'buslijn' more workable
from Functies_Bram import omloopplanning_buslijn
omloopplanning_buslijn(omloopplanning)

# Create dictionary with distances
afstand={}
for i in range(len(afstandsmatrix)):
    afstand[f"{afstandsmatrix['startlocatie'][i]}{afstandsmatrix['eindlocatie'][i]}{afstandsmatrix['buslijn'][i]}"]=afstandsmatrix['afstand in meters'][i]

# Add column afstandcode
from Functies_Bram import afstandcode_maken
afstandcode_maken(omloopplanning)
print(omloopplanning)