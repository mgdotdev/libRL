<h1><code>refactoring.py</code></h1>

# <h3>file_refactor</h3>

    libRL.refactoring.file_refactor(
        data=None, **kwargs
    )

Refactors the given user data into an actionable permittivity and
permeability array.

    :param data:   (data)

Permittivity and Permeability data of Nx5 dimensions. Can be a string
equivalent to the directory and file name of either a .csv or .xlsx of
Nx5 dimensions. Text above and below data array will be automatically
avoided by the program (most network analysis instruments report data
which is compatible with the required format)

    :param kwargs:  :override=:
                    (None); 'chi zero'; 'eps set'

provides response simulation functionality within libRL, common for
discerning which EM parameters are casual for reflection loss. 'chi
zero' sets mu = (1 - j·0). 'eps set' sets <br> epsilon = (avg(e1)-j·0).

    :return:        (data)        
    
refactored data data of Nx5 dimensionality in numpy array

# <h3>interpolate</h3>

    libRL.refactoring.file_refactor(
        data=None, **kwargs
    )

uses SciPy's interpolation module to generate interpolating functions
over the input data.

    :param data:   (data)   
    
Permittivity data of Nx5 form where N rows are 
[frequency, e1, e2, mu1, mu2]


    :param kwargs:  :interp=:
                    ('cubic'); 'linear'

Method for interpolation. Set to linear if user wants to linear interp
instead of cubic spline.

    :return:        e1f, e2f, mu1f, mu2f

returns four functions for Real Permittivity,
Complex Permittivity, Real Permeability, and
Complex Permeability respectively

# <h3>f_set_ref</h3>

    libRL.refactoring.file_refactor(
        f_set, data
    )

refactors the input f_set to the corresponding
Nx1 numpy array.

    :param f_set:   (start, end, [step])

tuple for frequency values in GHz

<P>
- or - 
</P>

- if given as tuple of len 3, results are interpolated
- if given as tuple of len 2, results are data-derived
with the calculation bound by the given start and end
frequencies from the tuple
- is given as int or float of len 1, results are
interpolated over the entire data set with a step size
of the given tuple value.
- if f_set is None (default), frequency is bound to
input data.

<space>

    :param data:   (data)

uses data as reference as frequencies are
experimentally determined.

    :return:        f_set
    
refactored f_set of type Nx1 numpy array.

# <h3>d_set_ref</h3>

    libRL.refactoring.file_refactor(
        d_set
    )

refactors the input d_set to the corresponding Nx1 numpy array.

    :param d_set:   (start, end, [step])

tuple for thickness values in mm.

<P>
- or - 
</P>

if d_set is of type list, then the thickness values
calculated will only be of the values present in the
list.

    :return:        d_set

refactored d_set of type Nx1 numpy array.

# <h3>m_set_ref</h3>

    libRL.refactoring.file_refactor(
        m_set
    )

refactors the input m_set to the corresponding Nx1 numpy array.

    :param m_set:   (start, end, [step])

tuple of ints which define the bands to be calculated.

<P>
- or - 
</P>

if m_set is given as a list [], the explicitly listed
band integers will be calculated.

<space>

    :return:        m_set
    
refactored m_set of type Nx1 numpy array.

# <h3>qgref</h3>

    libRL.refactoring.qgref(
        data
    )

grabs the passed directory location for image saving

    :param data:   (r'C:\file_directory')

Accepts data as a variable before data refactoring to the permittivity
and permeability array. As such, if data is passed as a file location,
qgref grabs the directory string from the file location and saves
resulting images at the directory. Else, the directory must be passed
directly.

    :return:        output_location
    
output directory for subsequent graphical figures.
