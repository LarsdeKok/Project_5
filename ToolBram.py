import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st
import numpy as np

# Read excel files
connection_data = pd.read_excel("Connexxion data - 2024-2025.xlsx")
omloopplanning = pd.read_excel("omloopplanning.xlsx")
dienstregeling = pd.read_excel("Connexxion data - 2024-2025.xlsx", sheet_name='Dienstregeling')
afstandsmatrix = pd.read_excel("Connexxion data - 2024-2025.xlsx", sheet_name='Afstandsmatrix')

# Fill blanks in 'Buslijn' with 'materiaalrit'
afstandsmatrix = afstandsmatrix.fillna('materiaalrit')

# Convert floats to integers and leave strings as is
afstandsmatrix['buslijn'] = afstandsmatrix['buslijn'].apply(lambda x: int(x) if isinstance(x, float) else x)

# In omloopplanning, make the column 'buslijn' more workable
omloopplanning['buslijn'] = omloopplanning['buslijn'].fillna('##')
for i in range(len(omloopplanning)):
    if omloopplanning['activiteit'][i]=='materiaal rit':
        omloopplanning['buslijn'][i].replace('##','materiaalrit')
omloopplanning['buslijn'] = omloopplanning['buslijn'].apply(lambda x: int(x) if isinstance(x, float) else x)
# Create dictionary with distances
afstand={}
for i in range(len(afstandsmatrix)):
    afstand[f"{afstandsmatrix['startlocatie'][i]}{afstandsmatrix['eindlocatie'][i]}{afstandsmatrix['buslijn'][i]}"]=afstandsmatrix['afstand in meters'][i]

