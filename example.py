import libRL
import pandas as pd
import matplotlib.pyplot as plt

'''    
this example file demonstrates how to use the included
functions available through the libRL library. Users are encouraged
to read the function descriptions for full context on the *args and 
**kwargs available. use 'for text in libRL.help(): print(text)' to
print out all help texts.
'''


def main():
    file_location = r'D:\Research and Teaching\University of Missouri-Kansas City\Dr. Xiaobo Chen\Microwave Absorption\Data\Al-TiO2'
    file_name = r'\Al-TiO2.xlsx'

    data = pd.ExcelFile(file_location + file_name).parse('700').to_numpy()[1:, :]

    reflection_loss = libRL.RL(
        Mcalc=data,
        f_set=(1,18,0.1),
        d_set=(1,5,0.1),
        interp='cubic',
        multiprocessing=0,
        multicolumn=True,
        as_dataframe=True
    )

    print(reflection_loss)

    characterization = libRL.CARL(
        Mcalc=data,
        f_set=(1,10,0.1),
        params='all',
        as_dataframe=True
    )

    print(characterization)

    band_analysis = libRL.BARF(
        Mcalc=data,
        f_set=(1,18,0.1),
        d_set=(1,20,0.1),
        m_set=(1,4,1),
        threshold=-10,
        as_dataframe=True
    )

    print(band_analysis)

    for text in libRL.help(): print(text)


if __name__ == "__main__":
    main()
