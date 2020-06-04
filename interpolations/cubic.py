import libRL
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

# data can be input using pandas to read an excel file containing 
# sheets for each measurement
data_file = r'D:\Research\University of Missouri-Kansas City\Dr. Xiaobo Chen\Microwave Absorption\Data\Polymers\Polypyrrole.xlsx'
data = pd.read_excel(data_file, sheet_name=None, skiprows=13, index_col=0)

# these correspond to the present sheets in the excel file
input_wt_pct = [5, 15, 25, 35]

# frequency values are consistent over all datasets, so just grab one for use
freqs = list(data['5'].index)

params = ['e1', 'e2', 'mu1', 'mu2']

# resulting interpolation is to be layered in a dictionary 
# containing the four parameters
func_dict = {p: dict() for p in params}

for c, p in enumerate(params):
    for i, f in enumerate(freqs):
        func_dict[p][f] = interp1d(
            x = [x for x in input_wt_pct],
            y = [data[str(x)].iloc[i, c] for x in input_wt_pct],
            kind = 'cubic' # cubic spline interpolation
        )

# function returns a theoretical DataFrame of the requested wt%
def res(wt):
    return pd.DataFrame({p: pd.Series(
        [func_dict[p][f](wt) for f in freqs],
        index=freqs
        ) for p in params}
    )
