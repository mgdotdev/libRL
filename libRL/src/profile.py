import time
from os import path
from itertools import cycle
from pathos.multiprocessing import ProcessPool as Pool
from libRL.src.tools import refactoring, quick_graphs
from libRL.src.reflection_loss import reflection_loss as rl
from libRL.src.characterization import characterization as char
from libRL.src.band_analysis import band_analysis as ba


def path_format(string):
    head, tail = path.split(string)
    if tail != '':
        return path.join(path_format(head), tail)
    else:
        return path.join(head, tail)

class Profile:
    """
Builds a dynamic profile class for work within a python environment.
    """
    def __init__(self, string):
        self.string = path_format(string)
        self.f_set = (
            self.data()[0,0],
            self.data()[-1,0],
            (self.data()[-1,0]-self.data()[0,0])/(self.data().shape[0]-1)
        ),
        self.d_set = (0,20,0.1)
        self.m_set = (1,5,1)
        self.params = 'all'
        self.threshold = -10
        
    def __str__(self):
        return path.split(self.string)[1]

    def __repr__(self):
        return r'libRL profile for data located at {}'.format(self.string)

    def data(self):
        return refactoring.file_refactor(self.string)

    def get_f(self):

        res = """
        start frequency: {} GHz,
        end frequency: {} GHz,
        step frequency: {} GHz
        """.format(self.f_set[0],self.f_set[1],self.f_set[2])

        return res

    def get_d(self):

        res = """
        start thickness: {} mm,
        end thickness: {} mm,
        step thickness: {} mm
        """.format(self.d_set[0],self.d_set[1],self.d_set[2])

        return res

    def get_m(self):

        res = """
        start band: band {},
        end band: band {},
        step band: band {}
        """.format(self.d_set[0],self.d_set[1],self.d_set[2])

        return res

    def get_thrs(self):
        res = 'band analysis threshold: {}'.format(self.threshold)
        return res

    def get_params(self):

        if self.params == 'all':
            param_list = [
                "tgde", "tgdu", "Qe", "Qu", "Qf",
                "ReRefIndx", "ExtCoeff",
                "AtnuCnstNm", "AtnuCnstdB",
                "PhsCnst", "PhsVel", "Res",
                "React", "Condt", "Skd", "Eddy"
            ]
        
        else:
            param_list = self.params

        res = 'params for calculation:'

        for param in param_list:
            res += param
            
        return res

    def interpolation(self):
        functions = refactoring.interpolate(self.data())
        func_dict = dict(zip(['e1','e2','mu1','mu2'], functions))
        return func_dict

    def reflection_loss(self, *args, **kwargs):
        
        res = rl(
            data=self.string, 
            f_set=self.f_set,
            d_set=self.d_set,
            **kwargs
        )

        return res

    def characterization(self, *args, **kwargs):

        res = char(
            data=self.string,
            f_set=self.f_set,
            params=self.params,
            **kwargs
        )

        return res

    def band_analysis(self, *args, **kwargs):

        res = ba(
            data=self.string,
            f_set=self.f_set,
            d_set=self.d_set,
            m_set=self.m_set,
            threshold=self.threshold,
            **kwargs
        )

        return res