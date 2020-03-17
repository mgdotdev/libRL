import time
from pandas import DataFrame
from libRL.src.tools import refactoring, quick_graphs
from pathos.multiprocessing import ProcessPool as Pool
from numpy import(
    array, zeros, arange
)


def f_peak(
    data=None, f_set=None,
    d_set=None, m_set=None,
    **kwargs
    ):

    # data is refactored into a Nx5 numpy array by the file_refactor
    # function from 'refactoring.py'

    start_time = time.time()
    file_name = 'results'

    overview = {
        'function': 'f_peak',
        'date/time': time.strftime('%D %H:%M:%S', time.localtime()),
        'd_set': str(d_set),
        'f_set': str(f_set),
        '**kwargs': str(kwargs)
    }

    if 'quick_save' in kwargs and kwargs['quick_save'] is True:
        kwargs['quick_save'], file_name = refactoring.qref(data)
        kwargs['as_dataframe'] = True
        kwargs['multicolumn'] = True

    if 'quick_graph' in kwargs and kwargs['quick_graph'] is True:
        kwargs['quick_graph'], file_name = refactoring.qref(data)

    data = refactoring.file_refactor(data, **kwargs)

    # acquire the desired interpolating functions from 'refactoring.py'
    e1f, e2f, mu1f, mu2f = refactoring.interpolate(data, **kwargs)

    # refactor the data sets in accordance to refactoring protocols
    # in 'refactoring.py'
    f_set = refactoring.f_set_ref(f_set, data)
    d_set = refactoring.d_set_ref(d_set)
    m_set = refactoring.m_set_ref(m_set)

    # construct a data grid for mapping from refactored data sets
    # d *must* be first as list comprehension cycles through f_set
    # for each d value, and this is deterministic of the structure
    # of the resultant.

    grid = [(e1f, e2f, mu1f, mu2f, m, n)
            for n in d_set
            for m in f_set
            ]

    if 'multiprocessing' in kwargs and int(kwargs['multiprocessing']) > 0:

        if kwargs['multiprocessing'] is True:
            pool = Pool()
            res = array(pool.map(
                refactoring.reflection_loss_function, grid
                ))
            pool.close()
        else:
            pool = Pool(nodes=int(kwargs['multiprocessing']))
            res = array(pool.map(
                    refactoring.reflection_loss_function, grid
                    ))
            pool.close()
        
    else:
        res = array(list(map(
            refactoring.reflection_loss_function, grid
            )))    

    # get frequency values from grid so
    # to normalize the procedure due to the
    # various frequency input methods
    gridInt = int(len(grid) / len(d_set))

    # zero-array of NxM where N is the frequency
    # values and M is 3 times the
    # number of thickness values
    MCres = zeros(
        (gridInt, d_set.shape[0] * 3)
    )

    # map the Zx3 result array to the NxM array
    for i in arange(int(MCres.shape[1] / 3)):
        MCres[:, 3 * i:3 * i + 3] = res[
            i * gridInt:(i + 1) * gridInt, 0:3
        ]

    # stick the MultiColumn Array in the place of the results array
    res = MCres[:, ::3]

    bool_matrix = zeros(res.shape)

    grid = [(row, col)
        for row in range(len(f_set))
        for col in range(len(d_set))
    ]

    out_cord = list()

    for row, col in grid:
        try:
            if res[row, col] < res[row+1, col] and      \
                res[row, col] < res[row, col+1] and     \
                res[row, col] < res[row-1, col] and     \
                res[row, col] < res[row, col-1]:
                bool_matrix[row, col] = 1
                out_cord.append([f_set[row],d_set[col]])
        except:
            pass

    if 'quick_save' in kwargs:
        refactoring.save_to_excel(
            array(out_cord).transpose(),
            kwargs['quick_save'],
            file_name,
            'f_peak',
            overview 
        )

    return out_cord
