from numpy import(
zeros, abs, argmin,
nan_to_num, where
)

import cmath
import warnings
from scipy.interpolate import interp1d

# typical RL function, return the real portion to truncate the complex portion
# (which is always j*0)
cpdef G(e1, e2, mu1, mu2, f, d):
    y = (20 * cmath.log10((abs(((1 * (cmath.sqrt((mu1 - cmath.sqrt(-1) * mu2) /
        (e1 - cmath.sqrt(-1) * e2))) * (cmath.tanh(cmath.sqrt(-1) * (2 * cmath.pi * (f * 10**9) * (d * 0.001) / 299792458) *
        cmath.sqrt((mu1 - cmath.sqrt(-1) * mu2) * (e1 - cmath.sqrt(-1) * e2))))) - 1) /
        ((1 * (cmath.sqrt((mu1 - cmath.sqrt(-1) * mu2) / (e1 - cmath.sqrt(-1) * e2))) *
        (cmath.tanh(cmath.sqrt(-1) * (2 * cmath.pi * (f * 10**9) * (d * 0.001) / 299792458) * cmath.sqrt(
        (mu1 - cmath.sqrt(-1) * mu2) * (e1 - cmath.sqrt(-1) * e2))))) + 1)))))
    return y.real

cpdef BARC(PnPGrid, mGrid, m_set, d_set, threshold):

    # PnP is the Nx5 grid of (freq, e1, e2, mu1, mu2)
    # mGrid is the d values associated with the quarter wavelength for the frequencies in PnP
    # d_set is the d_set values (duh).

    cdef int cnt0
    cdef int cnt1

    # you're going to get an annoying warning from the interpolation of the lower
    # first bound, because in d(f) the result of 2m-2 is 0 for m being 1, the first
    # band. This is of no consequence to  the actual calculation though since the
    # included computation corrects for this instance by pushing the starting freq
    # value to PnPGrid[0,0] when the requested frequency is outside the data range.

    warnings.filterwarnings('ignore')

    res = zeros((d_set.shape[0], m_set.shape[0]))

    for cnt0 in range(m_set.shape[0]):

        # functionalize every 2 col of mGrid to yield a frequency value for the
        # lower and upper index bounds.

        DtoFlow = interp1d(
            mGrid[:, 2*cnt0], PnPGrid[:, 0],
            kind='linear', fill_value='extrapolate'
        )

        DtoFhigh = interp1d(
            mGrid[:, 2*cnt0+1], PnPGrid[:, 0],
            kind='linear', fill_value='extrapolate'
        )

        for cnt1 in range(d_set.shape[0]):

            # determine the band boundaries from the interpolation function.
            f_init_low = float(DtoFlow(d_set[cnt1]))
            f_init_high = float(DtoFhigh(d_set[cnt1]))

            # if either value is outside the potential (f, d) grid space, truncate
            # at the grid space edge so to not erroneously extrapolate.
            if f_init_low < PnPGrid[0,0]:
                f_init_low = PnPGrid[0,0]

            if f_init_high > PnPGrid[-1,0]:
                f_init_high = PnPGrid[-1,0]

            # determine the associated indexes within PnPGrid.
            upper_index = argmin(abs(f_init_high - PnPGrid[:,0]))
            lower_index = argmin(abs(f_init_low - PnPGrid[:,0]))

            # for the freq values within the band boundaries, if the associated
            # reflection loss is below the threshold, increase the band_count.
            # band_count starts at -1 because a single point below the threshold
            # doesn't constitute a span.
            band_count = -1
            for val in range(lower_index,upper_index):
                if G(
                PnPGrid[val, 1], PnPGrid[val, 2], PnPGrid[val, 3],
                PnPGrid[val, 4], PnPGrid[val, 0], float(d_set[cnt1])
                ) < threshold:
                    band_count += 1

            # resultant is the product of the band count and the step size.
            res[cnt1, cnt0] = band_count*(
            (PnPGrid[upper_index,0] - PnPGrid[lower_index,0])/(
            PnPGrid[lower_index:upper_index].shape[0]-1))

            # clean up data
            res = nan_to_num(res, nan=0)
            res = where(res<0, 0, res)

    return res

