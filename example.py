'''
this example file demonstrates how to use the included
functions available through the libRL library. Users are encouraged
to call/read the docstrings for descriptions and full context on the
*args and **kwargs available.
'''

import libRL
from os import path
import pandas as pd

def main():

    import_file = path.join(
        path.abspath(path.dirname(__file__)),
        'test',
        'test_data.xlsx'
    )

    dataset = pd.read_excel(import_file).to_numpy()

    reflection_loss = libRL.reflection_loss(
        data=dataset,
        f_set=(1,18,1),
        d_set=(0,20,1),
        interp='cubic',
        multiprocessing=True,
        multicolumn=True,
        as_dataframe=True,
        quick_graph=False
    )

    print(reflection_loss)

    characterization = libRL.characterization(
        data=dataset,
        f_set=(1,18,1),
        params=['eddy'],
        as_dataframe=True
    )

    print(characterization)

    band_analysis = libRL.band_analysis(
        data=dataset,
        f_set=(1,18,1),
        d_set=(1,5,0.1),
        m_set=[1,2,3,4,5],
        thrs=-10,
        as_dataframe=True,
        quick_graph=False
    )

    print(band_analysis)


if __name__ == "__main__":
    main()
