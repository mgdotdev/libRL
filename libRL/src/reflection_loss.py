import time
from pandas import DataFrame
from libRL.src.tools import refactoring, quick_graphs
from pathos.multiprocessing import ProcessPool as Pool
from numpy import(
    array, zeros, arange
)


def reflection_loss(
        data=None, f_set=None,
        d_set=None, **kwargs
):
    """

The reflection_loss (RL) function calculates the RL based on the mapping
passed through as the grid variable, done either through multiprocessing
or through the python built-in map() function. The RL function always
uses the interpolation function, even though as the function passes
through the points associated with the input data, solving for the
function at the associated frequencies yields the data point. This
is simply for simplicity.

ref: https://doi.org/10.1016/j.jmat.2019.07.003

::

    :param data:   (data)

Permittivity and Permeability data of Nx5 dimensions. Can be a string
equivalent to the directory and file name of either a .csv or .xlsx of Nx5
dimensions. Text above and below data array will be automatically avoided by
the program (most network analysis instruments report data which is compatible
with the required format)

::

    :param f_set:   (start, end, [step])

tuple for frequency values in GHz

- if given as list of len 3, results are interpolated
- if given as list of len 2, results are data-derived with the calculation
  bound by the given start and end frequencies
- if f_set is None, frequency is bound to input data

::

    :param d_set:   (start, end, step)

tuple for thickness values in mm.

- if d_set is of type list, then the thickness values calculated will only be
  of the values present in the list.

::

    :param kwargs:  interp=
                    ('cubic'); 'linear'

Method for interpolation. Set to linear if user wants to linear interp instead
of cubic spline. Default action uses cubic spline.

::

    :param kwargs:  override=
                    (None); 'chi zero', 'eps set'

provides response simulation functionality within libRL, common for discerning
which EM parameters are casual for reflection loss. 'chi zero' sets
mu = (1 - j*0). 'eps set' sets epsilon = (avg(e1)-j*0).

::

    :param kwargs:  multiprocessing=
                    (False); True, 0, 1, 2, ...

Method for activating multiprocessing functionality for faster run times. This
kwarg takes integers and booleans. Set variable to True to use all
available nodes. Pass an integer value >1 to use (int) nodes. Will properly 
handle 'False' as an input though it's equivalent to not even designating the
particular kwarg.

NOTE: if you use the multiprocessing functionality herein while on a Windows
computer you ***MUST MUST MUST MUST*** provide main module protection via the
:code:`if __name__ == "__main__":` conditional so to negate infinite spawns.

::

    :param kwargs:  quick_graph=
                    (False); True, 'show', str()

Generates a `.png` graphical image to a specified location. If set to True, the
quick_graph function saves the resulting graphical image to the location of the
input data as defined by the data input (assuming that the data was input via a
location string. If not, True throws an assertion error). The raw string of a
file location can also be passed as the str() argument, if utilized then the
function will save the graph at the specified location. Optionally, this kwarg
can be set to 'show' to simply display the generated image to either a 
matplotlib window on the desktop or within a jupyter notebook if the function
is run on google colab.

::

    :param kwargs:  as_dataframe=
                    (False); True

returns data in a pandas dataframe. This is particularly useful if multicolumn
is also set to true.

::

    :param kwargs:  multicolumn=
                    (False); True

outputs data in multicolumn form with  a numpy array of [RL, f, d] iterated
over each of the three columns.

- if as_dataframe is used, then return value will be a pandas dataframe with
  columns of name d and indexes of name f.

::

    :param kwargs:  quick_save=
                    (False); True, str()

Saves the results to an excel file for external reference. If set to True, the
quick_save function saves the resulting excel file to the location of the
input data as defined by the data input (assuming that the data was input via a
location string. If not, True throws an assertion error). The raw string of a
file location can also be passed as the str() argument, if utilized then the
function will save the excel file at the specified location.

::

    :return:        [RL, f, d]

returns Nx3 data set of [RL, f, d] by default

- if multicolumn=True, an NxM dataframe with N rows for the input frequency
  values and M columns for the input thickness values, with pandas dataframe
  headers/indexes of value f/d respectively.
    """
    # data is refactored into a Nx5 numpy array by the file_refactor
    # function from 'refactoring.py'

    start_time = time.time()
    file_name = 'results'

    overview = {
        'function': 'reflection_loss',
        'date/time': time.strftime('%D %H:%M:%S', time.localtime()),
        'd_set': str(d_set),
        'f_set': str(f_set),
        '**kwargs': str(kwargs)
    }

    if 'quick_save' in kwargs:
        if kwargs['quick_save'] is True:
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

    # construct a data grid for mapping from refactored data sets
    # d *must* be first as list comprehension cycles through f_set
    # for each d value, and this is deterministic of the structure
    # of the resultant.
    grid = [(e1f, e2f, mu1f, mu2f, m, n)
            for n in d_set
            for m in f_set
            ]

    # if multiprocessing is given as True use all available nodes
    # if multiprocessing is given and is a non-zero
    # integer, use int value for number of nodes
    # if multiprocessing is given as anything else, ignore it.
    # returns res of Zx3 data where Z is the product
    # of len(f_set) and len(d_set)

    if 'multiprocessing' in kwargs and int(kwargs['multiprocessing']) > 0:

        if kwargs['multiprocessing'] is True:
            with Pool() as pool:

                res = array(pool.map(
                    refactoring.reflection_loss_function, grid
                    ))


        else:
            with Pool(nodes=int(kwargs['multiprocessing'])) as pool:

                res = array(pool.map(
                        refactoring.reflection_loss_function, grid
                        ))
        
    else:
        res = array(list(map(
            refactoring.reflection_loss_function, grid
            )))

    # takes data derived from computation and the file directory string and
    # generates a graphical image at the at location.
    if 'quick_graph' in kwargs and isinstance(
            kwargs['quick_graph'], str
            ) is True:

        quick_graphs.quick_graph_reflection_loss(
            results=res, location=kwargs['quick_graph']
            )

    # formatting option, sometimes professors
    # like 3 columns for each thickness value
    if 'multicolumn' in kwargs and kwargs['multicolumn'] is True:

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
        res = MCres

    if 'as_dataframe' in kwargs and kwargs['as_dataframe'] is True:

        if 'multicolumn' in kwargs and kwargs['multicolumn'] is True:
            res = DataFrame(res[:, ::3])
            res.columns = list(d_set)
            res.index = list(f_set)

        else:
            res = DataFrame(res)
            res.columns = ['RL', 'f', 'd']

        if 'quick_save' in kwargs and isinstance(
                kwargs['quick_save'], str
                ) is True:
                
            stats = (
                    res[res.min().idxmin()][res.min(axis=1).idxmin()],
                    'frequency='+str(res.min(axis=1).idxmin()),
                    'thickness='+str(res.min().idxmin())
                    )

            overview.update({
                    'calculation time': time.time()-start_time,
                    'maxRL': str(stats)
                })

            overview = DataFrame.from_dict(overview, orient='index')

            refactoring.save_to_excel(
                data=res,
                location=kwargs['quick_save'],
                file_name=file_name,
                parent='reflection_loss',
                overview=overview
            )

    return res
