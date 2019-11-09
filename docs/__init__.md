<h1> <code> __init__.py </code> </h1>

# <h3>reflection_loss</h3>

    libRL.reflection_loss(
        data=None, f_set=None, d_set=None, **kwargs
    )

the reflection_loss (RL) function calculates the RL based on the mapping
passed through as the grid variable, done either through multiprocessing
or through the python built-in map() function. The RL function always
uses the interpolation function, even though as the function passes
through the points associated with the input data, solving for the
function at the associated frequencies yields the data point. This
is simply for simplicity.

Reference: <br>
[*Recent Progress in Nanomaterials for Microwave Absorption*](https://doi.org/10.1016/j.jmat.2019.07.003)

    :param data:   (data)

Permittivity and Permeability data of Nx5 dimensions.
Can be a string equivalent to the directory and file
name of either a .csv or .xlsx of Nx5 dimensions. Text
above and below data array will be automatically
avoided by the program (most network analysis instruments
report data which is compatible with the required format)

    :param f_set:   (start, end, [step])

tuple for frequency values in GHz

<P>
- or - 
</P>

- if given as list of len 3, results are interpolated
- if given as list of len 2, results are data-derived
with the calculation bound by the given start and end
frequencies
- if f_set is None, frequency is bound to input data

    :param d_set:   (start, end, step)

tuple for thickness values in mm.

<P>
- or - 
</P>

- if d_set is of type list, then the thickness values
calculated will only be of the values present in the
list.

<space>

    :param kwargs:  :interp=:
                    ('cubic'); 'linear'

Method for interpolation. Set to linear if user wants to
linear interp instead of cubic spline. Default action
uses cubic spline.

    :param kwargs:  :override=:
                    (None); 'chi zero'; 'eps set'

provides response simulation functionality within libRL, common for
discerning which EM parameters are casual for reflection loss. 'chi
zero' sets mu = (1-j·0). 'eps set' sets epsilon = (avg(e1)-j·0).

    :param kwargs:  :multiprocessing=:
                    (False); True; 0; 1; 2; ...

Method for activating multiprocessing functionality for
faster run times. This `**kwarg` takes integers and booleans.
Set variable to True or 0 to use all available nodes. Pass
an integer value to use (int) nodes. Will properly handle
'False' as an input though it's equivalent to not even
designating the particular `**kwarg`.

NOTE: if you use the multiprocessing functionality herein while on a
Windows computer you ***MUST MUST MUST MUST*** provide main module
protection via the if `__name__ == "__main__":` conditional so to negate
infinite spawns.

    :param kwargs:  :quick_graph=:
                    (False); True, str()

saves a *.png graphical image to a specified location. If set to True,
the quick_graph function saves the resulting graphical image to the
location of the input data as defined by the data input (assuming that
the data was input via a location string. If not, True throws an
assertion error). The raw string of a file location can also be passed
as the str() argument, if utilized then the function will save the graph
at the specified location.

    :param kwargs:  :as_dataframe=:
                    (False); True

returns data in a pandas dataframe. This is particularly useful if
multicolumn is also set to true.

    :param kwargs:  :multicolumn=:
                    (False); True

outputs data in multicolumn form with  a numpy array of
[RL, f, d] iterated over each of the three columns.

<P>
- or - 
</P>

if as_dataframe is used, then return value will be a pandas dataframe
with columns of name d and indexes of name f.

    :return: 
    
Nx3 data set of [RL, f, d] by default

<P>
- or - 
</P>

if multicolumn=True, an NxM dataframe with N rows for the input
  frequency values and M columns for the input thickness values, with
  pandas dataframe headers/indexes of value f/d respectively.

---

# <h3>characterization</h3>

    libRL.characterization(
        data=None, f_set=None, params="all", **kwargs
    )

the characterization function takes a set or list of keywords in the
'params' variable and calculates the character values associated with
the parameter. See 10.1016/j.jmat.2019.07.003 for further details and
the function comments below for a full list of keywords.

Reference: <br>
[*Recent Progress in Nanomaterials for Microwave Absorption*](https://doi.org/10.1016/j.jmat.2019.07.003)

    :param data: (data)

Permittivity and Permeability data of Nx5 dimensions.
Can be a string equivalent to the directory and file
name of either a .csv or .xlsx of Nx5 dimensions. Text
above and below data array will be automatically
avoided by the program (most network analysis instruments
report data which is compatible with the required format)

    :param f_set:   (start, end, [step])

tuple for frequency values in GHz

<P>
- or - 
</P>

- if given as list of len 3, results are interpolated
- if given as list of len 2, results are data-derived with the 
  calculation bound by the given start and end frequencies.
  
- if f_set is None, frequency is bound to input data
- if f_set is of type list, the frequencies calculate will be only the
  frequencies represented in the list.

<space>
 
    :param params:
    
A list of string arguments for the parameters the user wants calculated.
                    
The available arguments are: 

    [
    "tgde",          # dielectric loss tangent
    "tgdu",          # magnetic loss tangent
    "Qe",            # dielectric quality factor
    "Qu",            # magnetic quality factor
    "Qf",            # total quality factor
    "ReRefIndx",     # Refractive Index
    "ExtCoeff",      # Extinction Coeffecient
    "AtnuCnstNm",    # Attenuation Constant (in Np/m)
    "AtnuCnstdB",    # Attenuation Constant (in dB/m)
    "PhsCnst",       # Phase Constant
    "PhsVel",        # Phase Velocity
    "Res",           # Resistance
    "React",         # Reactance
    "Condt",         # Conductivity
    "Skd",           # Skin Depth
    "Eddy"           # Eddy Current Loss
    ]

if 'all' (default) is passed, calculate everything.

    :param kwargs: :override=: 
                    (None); 'chi zero'; 'eps set'

provides response simulation functionality within libRL, common for
discerning which EM parameters are casual for reflection loss. 'chi
zero' sets mu = (1-j·0). 'eps set' sets epsilon = (avg(e1)-j·0).

    :param kwargs:  :as_dataframe=:
                    (False); True

returns the requested parameters as a pandas dataframe with column names
as the parameter keywords.

    :return:        
    
NxY data set of the requested parameters as columns 1 to Y with the
input frequency values in column zero to N. 

<P>
- or - 
</P>

returns a pandas DataFrame with the requested parameters as column
headers, and the frequency values as index headers.

---

# <h3>band_analysis</h3>

    libRL.band_analysis(
        data=None, f_set=None, d_set=None, m_set=None, threshold=-10, **kwargs
    )

the Band Analysis for ReFlection loss (BARF) function uses Permittivity
and Permeability data of materials so to determine the effective
bandwidth of Reflection Loss. The effective bandwidth is the span of
frequencies where the reflection loss is below some proficiency
threshold (standard threshold is -10 dB). Program is computationally
taxing; thus, efforts were made to push most of the computation to the
C-level for faster run times - the blueprints for such are included in
the cpfuncs.pyx file which is passed through pyximport().

`[and yes, I love you 3000]`

References: <br>
[*Microwave absorption of aluminum/hydrogen treated titanium dioxide nanoparticles*](https://doi.org/10.1016/j.jmat.2018.12.005)
<br>
[*Recent progress of nanomaterials for microwave absorption*](https://doi.org/10.1016/j.jmat.2019.07.003)
 
    :param data: (data)

Permittivity and Permeability data of Nx5 dimensions.
Can be a string equivalent to the directory and file
name of either a .csv or .xlsx of Nx5 dimensions. Text
above and below data array will be automatically
avoided by the program (most network analysis instruments
report data which is compatible with the required format)

    :param f_set: (start, end, [step])

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

    :param d_set: (start, end, [step])

tuple for thickness values in mm.
<P>
- or - 
</P>

- if d_set is of type list, then the thickness values
calculated will only be of the values present in the
list. (is weird, but whatever.)

<space>

    :param m_set: (start, end, [step])

tuple of ints which define the bands to be calculated.
<P>
- or - 
</P>

- if m_set is given as a list [], the explicitly listed
band integers will be calculated.

<space>

    :param thrs: -10

Threshold for evaluation. If RL values are below this threshold value,
the point is counted for the band. Typical threshold value is -10 dB.

    :param kwargs: :override=: 
                    (None); 'chi zero'; 'edp zero'; 'eps set'

provides response simulation functionality within libRL, common for
discerning which EM parameters are casual for reflection loss. 'chi
zero' sets mu = (1 - j·0). 'eps set' sets epsilon = (avg(e1)-j·0).

    :param kwargs:  :interp=:
                    ('cubic'); 'linear'

Method for interpolation. Set to linear if user wants to linear interp
instead of cubic spline.

    :param kwargs:  :quick_graph=:
                    (False); True; str()

saves a *.png graphical image to a specified location. If set to True,
the quick_graph function saves the resulting graphical image to the
location of the input data as defined by the data input (assuming that
the data was input via a location string. If not, True throws an
assertion error). The raw string of a file location can also be passed
as the str() argument, if utilized then the function will save the graph
at the specified location.

    :param kwargs:  :as_dataframe=:
                    (False); True

Formats results into a pandas
dataframe with the index labels as the thickness
values, the column labels as the band numbers, and
the dataframe as the resulting effective bandwidths.

    :return:        
    
returns len(3) tuple with [d_set, band_results, m_set].
the rows of the band_results correspond with the d_set and
the columns of the band_results correspond with the m_set.

<P>
- or - 
</P>

returns the requested dataframe with the band values as
column headers and the thickness values as row headers.
