<h1> <code> cpfuncs.pyx </code> </h1>

# <h3>band_analysis_cython</h3>

    libRL.cpfuncs.band_analysis_cython(
        PnPGrid, mGrid, m_set, d_set, thrs
    )

The band_analysis_cython function determines the band analysis of
materials by tallying the frequency points which satisfy the threshold,
and summing the span of their frequencies.

    :param PnPgrid: (data)
    
PnPgrid is a pre-processed permittivity & permeability array passed from
libRL.CARL of shape Nx5 of [freq, e1, e2, mu1, mu2].

    :param mGrid:   (data)
    
mGrid is a numpy array of d_values calculated from a modified
quarter-wavelength function determined from the frequency values of the
PnPgrid.

    :param m_set:   (data)
    
m_set is a numpy array of bands passed through from
libRL.refactoring.m_set_ref()

    :param d_set:   (data)
    
d_set is a numpy array of thickness values passed through from
libRL.refactoring.d_set_ref()

    :param thrs:    (data)
    
thrs is the threshold value to test Reflection loss against for each (f,
d) point in the response field, passed through directly from
libRL.band_analysis()

    :return:
    
the effective bandwidth for each thickness value across each requested
band.
