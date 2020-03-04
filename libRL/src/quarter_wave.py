import time, cmath
from pandas import DataFrame
from libRL.src.tools import refactoring, quick_graphs
from numpy import(
    array, zeros, arange
)


def quarter_wave(
    data=None, f_set=None,
    m_set=None, **kwargs
):

    start_time = time.time()
    file_name = 'results'

    overview = {
        'function': 'quarter_wave',
        'date/time': time.strftime('%D %H:%M:%S', time.localtime()),
        'f_set': str(f_set),
        'm_set': str(m_set),
        '**kwargs': str(kwargs)
    }

    if 'quick_save' in kwargs and kwargs['quick_save'] is True:
        kwargs['as_dataframe'] = True
        kwargs['quick_save'], file_name = refactoring.qref(data)
    
    data = refactoring.file_refactor(data, **kwargs)

    f_set = refactoring.f_set_ref(f_set, data)
    m_set = refactoring.m_set_ref(m_set)

    # acquire the desired interpolating functions from 'refactoring.py'
    e1f, e2f, mu1f, mu2f = refactoring.interpolate(data, **kwargs)

    def ref_index(f):
        y = cmath.sqrt(
            (mu1f(f)-cmath.sqrt(-1)*mu2f(f))*(e1f(f)-cmath.sqrt(-1)*e2f(f))
            )
        return y.real

    output = list()
    for m in m_set:

        def dfind_qw(f):
            y = (299792458/(f*(10**9)))*(1.0/ref_index(f))*(((2.0*m)-1.0)/4.0)
            return y*1000

        res = list(map(dfind_qw, f_set))
        output.append(res)

    dataset = array(output).transpose()

    if 'as_dataframe' in kwargs and kwargs['as_dataframe'] is True:
        dataset = DataFrame(dataset)
        dataset.columns = list(m_set)
        dataset.index = list(f_set)

        if 'quick_save' in kwargs and isinstance(kwargs['quick_save'], str) is True:

            overview.update({'calculation time': time.time()-start_time})

            overview = DataFrame.from_dict(overview, orient='index')

            refactoring.save_to_excel(
                data=dataset,
                location=kwargs['quick_save'],
                file_name=file_name,
                parent='quarter_wave',
                overview=overview
            )

    return dataset
