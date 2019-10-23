from os import path
import pytest
import libRL


def main():

    file_location = path.abspath(path.dirname(__file__))
    file_name = 'paraffin_data.csv'
    reflection_loss = libRL.RL(
        Mcalc=file_location+'\\'+file_name,
        f_set=(1, 18, 1),
        d_set=(1, 20, 1),
        interp='cubic',
        multiprocessing=False,
        multicolumn=True,
        as_dataframe=True
    )
    return reflection_loss


def test_main():
    assert main.shape == (18, 20)
