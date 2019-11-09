from os import path
import pytest
import libRL


def main():

    data_url = 'https://raw.githubusercontent.com/' \
           '1mikegrn/libRL/master/test/test_data.csv'

    reflection_loss = libRL.reflection_loss(
        data=data_url,
        f_set=(1, 18, 1),
        d_set=(1, 20, 1),
        interp='cubic',
        multiprocessing=False,
        multicolumn=True,
        as_dataframe=True
    )

    characterization = libRL.characterization(
        data=data_url,
        f_set=(1,18,1),
        params='all',
        as_dataframe=True
    )

    band_analysis = libRL.band_analysis(
        data=data_url,
        f_set=(1,18,1),
        d_set=(1,20,1),
        m_set=[1,2,3,4,5],
        thrs=-10,
        as_dataframe=True
    )

    return reflection_loss.shape, characterization.shape, band_analysis.shape


def test_main():
    check = main()
    assert check == ((18, 20), (18, 16), (20, 5))

