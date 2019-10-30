'''
this example file demonstrates how to use the included
functions available through the libRL library. Users are encouraged
to call/read the docstrings for descriptions and full context on the
*args and **kwargs available.
'''

import libRL
from os import path


def main():

    import_file = path.abspath(
        path.dirname(__file__)
    ) + r'\test\test_data.xlsx'

    reflection_loss = libRL.RL(
        Mcalc=import_file,
        f_set=(2,18),
        d_set=(0,20,1),
        interp='cubic',
        multiprocessing=True,
        multicolumn=True,
        as_dataframe=True,
    )

    print(reflection_loss)

    characterization = libRL.CARL(
        Mcalc=import_file,
        f_set=(1,10),
        params='all',
        as_dataframe=True
    )

    print(characterization)

    band_analysis = libRL.BARF(
        Mcalc=import_file,
        f_set=(1,18),
        d_set=(1,5,0.1),
        m_set=[1,2,3,4,5],
        thrs=-20,
        as_dataframe=True,
    )

    print(band_analysis)


if __name__ == "__main__":
    main()
