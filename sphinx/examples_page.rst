Examples
========

Here we're going to demonstrate how to call the various functions of the
libRL library - both making use of the main functions as well as calling
some of the subdirectories that researchers may have interest in.

Windows
-------

Suppose that from experimentation a researcher has generated a
'paraffin_data.csv' file of the following structure:

::

    Transmission Line And Free Space Method 16.0.16092801,,,,
    Agilent Technologies,E5063A,MY54100168,A.03.71,
    ,,,,
    Ch 1,,,,
    Ports:, 1 & 2,,,
    Measurement Model:, Reflection/Transmission Mu and Epsilon,,,
    Sample Holder Type:, Coax/TEM,,,
    Sample Holder Length:, 99.700000 mm,,,
    Distance to Sample:, 43.600000 mm,,,
    Sample Thickness:, 3.040000 mm,,,
    ...
    ...
    ...  
    Date:,"Thursday, January 25, 2018 14:10:19",,,
    frequency(GHz),e',e'',u',u''
    1,2.1976,0.062033333,1.0705,0.063966667
    1.34,2.1814,0.0554,1.0681,0.0577
    1.68,2.1444,0.0631,1.0942,0.0339
    2.02,2.132,0.0493,1.0997,0.0364
    2.36,2.1389,0.0457,1.09,0.0281
    ...
    ...
    ...  
    16.98,2.202,0.0513,1.0237,-0.0016
    17.32,2.19738,0.0587,1.023466667,-0.00285
    17.66,2.191617143,0.06263,1.02912381,-0.00323
    18,2.185854286,0.06656,1.034780952,-0.00361

This is a typical Nx5 .csv instrument file that researchers might have
generated from network analysis (Note: libRL is written to handle
tab-separated .csv files as well as .xlsx files)

Let's further suppose that this file is located on the desktop, such
that the full file path for our data file is the following:

::

    C:\Users\1mike\Desktop\paraffin_data.csv

libRL is designed to parse this data file directly from its
instrumentation file. To use libRL in RAM analysis, we can simply
construct the following script in our favorite IDE to calculate, for
example, the reflection loss (RL) as a unit of decibel defined as:

.. math::

    RL(dB) = 20 \cdot log_{10}\Bigg|{\frac{Z_{in}(f, d)-1}{Z_{in}(f,
    d)+1}}\Bigg|


.. math::

    Z_{in}(f, d) =
    \Bigg[ \frac{\mu'(f) - j \cdot \mu''(f)}{\epsilon'(f) - j \cdot \epsilon''(f)} \Bigg]^{\frac{1}{2}}
    \cdot tanh \Bigg( j \cdot \frac{2\pi f \cdot d}{c}
    \{[\mu'(f) - j \cdot \mu''(f)][\epsilon'(f) - j \cdot \epsilon''(f)] \}
    ^{\frac{1}{2}} \Bigg)

can be calculated from the following script:

::

    import libRL
    
    results = libRL.reflection_loss(
        data=r'C:\Users\1mike\Desktop\paraffin_data.csv',
        d_set=[3.04]
    )
    
This represents the minimal computable function that libRL will
calculate over. At minimum, the permittivity and permeability data
should be passed, as well as the thickness parameters for calculation
[this should make intuitive sense, as RL is calculated over an
(f, d) grid space]. The resulting data set is a Nx3 numpy array
of the Reflection Loss, frequencies, and thicknesses in columns
0, 1, 2 respectively.

Of course, libRL is designed to do much more than just this minimal
computation. As permittivity and permeability are farads/meter and
henries/meter, the thickness parameter is decoupled from experimentation
and thus can be used to calculate RL of thicknesses not explicitly used
in measurement. As such, we can pass a *tuple* of thickness values to
generate an array in accordance to numpy.arange()

::

    import libRL
    
    results = libRL.reflection_loss(
        data=r'C:\Users\1mike\Desktop\paraffin_data.csv',
        d_set=(0,5,1)
    )
    
This results in the calculation being mapped over the thickness range of
0-5 mm (libRL *includes* the upper bound here) at every step of 1 mm.

Currently, reflection loss is being calculated using the frequency
values in the permittivity and permeability data set. libRL has a
protocol however which allows the user to *interploate* the data such
that frequency can be controlled similarly to the thicknesses.

::

    import libRL
    
    results = libRL.reflection_loss(
        data=r'C:\Users\1mike\Desktop\paraffin_data.csv',
        f_set=(1,18,1),
        d_set=(0,5,1)
    )
    
Here, the resulting calculation returns a data set calculated over the
ranges of 1-18 GHz, 0-5 mm at 1 unit intervals. 

To note, libRL allows for *interpolation* and not *extrapolation*.
Attempts to use the interpolating functions outside of your experimental
bounds throws an error.

::

    Traceback (most recent call last):
      File "C:\Users\1mike\PycharmProjects\libRL\libRL\refactoring.py", line 252, in f_set_ref
        raise SyntaxError(error_msg)
    SyntaxError: f_set must be of order (start, stop, step) where 'start' and 'stop' are within the bounds of the data
    
There is a set of keyword arguments which libRL.reflection_loss accepts.
These keyword areguments are:

::

    interp=
    multiprocessing=
    multicolumn=
    as_dataframe=
    quick_graph=

Descriptions of these keyword arguments can be found in the docstrings.

The other functions available in the libRL library use the same
refactoring protocols for data, f_set, d_set, and m_set. They each have
their own keyword arguments and parameter arguments, so researchers are
encouraged to look at the documentation provided on this site for each
of those functions.

Some of the subdirectory functions available which are of convenient use
are the :func:`libRL.refactoring.file_refactor` and
:func:`libRL.refactoring.interpolate` functions,
which can be found in documentation under libRL/refactoring.py. In
:code:`file_refactor()` is the protocol libRL uses to parse
out the file string into actionable data, and :code:`interpolate()`
is the protocol libRL uses to generate the interpolation functions over
the actionable data set.

Linux
-----

*this page is still currently under construction. Check back shortly!*

macOS
-----

*this page is still currently under construction. Check back shortly!*
