## if __name__== __main__ voor tests
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as sp
import numpy as np


def aantal_bussen(planning):
    bussen = planning[planning.columns[len(planning.columns)-1]].unique()

