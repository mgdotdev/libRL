import libRL

'''    
this example file demonstrates how to use the included
functions available through the libRL library. Users are encouraged
to read the function descriptions for full context on the *args and 
**kwargs available.
'''


def main():
    file_location = r'D:\Research and Teaching\University of Missouri-Kansas City\Dr. Xiaobo Chen\Microwave Absorption\Data\(nBu4)2Mo6 {A}'
    file_name = r'\data1'

    reflection_loss = libRL.RL(
        Mcalc=file_location + file_name + '.csv',
        f_set=(1,10), d_set=(1,10,1), interp='linear',
        multiprocessing=0, multicolumn=True
    )

    characterization = libRL.CARL(
        Mcalc=file_location + file_name + '.csv',
        f_set=(1,10,0.1), params='All', as_dataframe=True
    )


if __name__ == "__main__":
    main()
