import libRL
import pandas as pd
import matplotlib.pyplot as plt

'''    
this example file demonstrates how to use the included
functions available through the libRL library. Users are encouraged
to read the function descriptions for full context on the *args and 
**kwargs available.
'''


def main():
    file_location = r'D:\Research and Teaching\University of Missouri-Kansas City\Dr. Xiaobo Chen\Microwave Absorption\Data\Al-TiO2'
    file_name = r'\Al-TiO2.xlsx'

    # reflection_loss = libRL.RL(
    #     Mcalc=file_location + file_name + '.xlsx',
    #     f_set=(1,18,0.1), d_set=(1,5,0.1), interp='linear',
    #     multiprocessing=0, multicolumn=True, as_dataframe=True
    # )

    # characterization = libRL.CARL(
    #     Mcalc=file_location + file_name + '.csv',
    #     f_set=(1,10,0.1), params='All', as_dataframe=True
    # )

    data = pd.ExcelFile(file_location+file_name).parse('700').to_numpy()[1:,:]

    band_analysis = libRL.BAR(
        Mcalc=data,
        f_set=(1,18,0.1), d_set=(1,4,0.1),
        m_set=(1, 1, 1), threshold=-10
    )

    print(band_analysis)

    plt.plot(band_analysis[0], band_analysis[1])
    plt.show()



if __name__ == "__main__":
    main()
