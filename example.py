'''
this example file demonstrates how to use the included
functions available through the libRL library. Users are encouraged
to call/read the docstrings for descriptions and full context on the
*args and **kwargs available.
'''

import libRL
import pandas as pd


def main():
    file_location = r'D:\Research and Teaching\University of Missouri-Kansas City\Dr. Xiaobo Chen\Microwave Absorption\Data\Al-TiO2'
    file_name = r'\Al-TiO2.xlsx'

    data = pd.ExcelFile(file_location + file_name).parse('700').to_numpy()[1:, :]

    import_file = r'C:\Users\1mike\PycharmProjects\libRL package\test\paraffin_data.csv'

    reflection_loss = libRL.RL(
        Mcalc=import_file,
        f_set=(1,20),
        d_set=[1,2,5],
        interp='cubic',
        multiprocessing=True,
        multicolumn=True,
        as_dataframe=True
    )

    print(reflection_loss)

    characterization = libRL.CARL(
        Mcalc=data,
        f_set=(1,10),
        params='all',
        as_dataframe=True
    )

    print(characterization)

    band_analysis = libRL.BARF(
        Mcalc=data,
        f_set=(1,10),
        d_set=[1,2,5],
        m_set=[1,2,5],
        thrs=-10,
        as_dataframe=True
    )

    print(band_analysis)


if __name__ == "__main__":
    main()
