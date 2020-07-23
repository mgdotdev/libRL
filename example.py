'''
this example file demonstrates how to use the included
functions available through the libRL library. Users are encouraged
to call/read the docstrings for descriptions and full context on the
*args and **kwargs available, or read the documentation available the following
websites:

Overview:
https://1mikegrn.github.io/libRL/

examples:
https://1mikegrn.github.io/libRL/#examples
'''

import libRL
import pandas as pd
from os import path

import glob

def main():
    """

this example script is designed to run a demonstration of each of the
available functions in libRL. Data is imported directly from the GitHub
repository for convenience. Results are simply printed.

    :return: nothing

    """

    files = glob.glob(r'C:\Users\1mike\Desktop\results\**.csv')

    for f in files:

        data_string = f

        reflection_loss = libRL.reflection_loss(
            data=data_string,
            f_set=(1,18,0.1),
            d_set=(0,20,0.1),
            interp='cubic',
            multicolumn=True,
            as_dataframe=True,
            quick_save=True,
            quick_graph=True
        ) 

        print(reflection_loss)

        characterization = libRL.characterization(
            data=data_string,
            f_set=(1,18,0.1),
            params='all',
            as_dataframe=True       
        )

        print(characterization)

        band_analysis = libRL.band_analysis(
            data=data_string,
            f_set=(1,18,0.1),
            d_set=(1,5,0.1),
            m_set=[1,2,3,4,5],
            thrs=-10,
            as_dataframe=True,
            quick_save=True,
            quick_graph=True            
        )

        print(band_analysis)

if __name__ == "__main__":
    main()