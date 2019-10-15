from numpy import(
zeros, abs, argmin
)

import cmath
from scipy.interpolate import interp1d

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
    # d_set is the d_set values (duh)

    cdef int cnt0
    cdef int cnt1

    res = zeros((d_set.shape[0], m_set.shape[0]))

    for cnt0 in range(m_set.shape[0]):

        # functionalize the boundaries, run the calculation over the entire space within the boundaries
        # adding the number of points which are below the threshold

        # functionalize mGrid to yield a frequency value for input thickness value
        DtoF = interp1d(
            mGrid[:, cnt0], PnPGrid[:, 0],
            kind='linear', fill_value='extrapolate'
        )

        for cnt1 in range(d_set.shape[0]):

            f_init = float(DtoF(d_set[cnt1]))

            if f_init > PnPGrid[0,0] and f_init < PnPGrid[-1, 0]:

                # find f in PnPGrid
                index = argmin(abs(f_init - PnPGrid[:,0]))
                upper_index, lower_index = index, index

                # parse out the bounds
                upper_bound, lower_bound = PnPGrid[upper_index, 0], PnPGrid[lower_index, 0]

                # push the upper bound
                while G(
                PnPGrid[upper_index, 1], PnPGrid[upper_index, 2], PnPGrid[upper_index, 3],
                PnPGrid[upper_index, 4], PnPGrid[upper_index, 0], float(d_set[cnt1])
                ) < threshold:
                    upper_bound = PnPGrid[upper_index, 0]
                    upper_index += 1
                    if upper_index == PnPGrid.shape[0]:
                        break

                while G(
                PnPGrid[lower_index, 1], PnPGrid[lower_index, 2], PnPGrid[lower_index, 3],
                PnPGrid[lower_index, 4], PnPGrid[lower_index, 0], float(d_set[cnt1])
                ) < threshold:
                    lower_bound = PnPGrid[lower_index, 0]
                    lower_index -= 1
                    if lower_index == -1:
                        break

                res[cnt1, cnt0] = upper_bound - lower_bound

    return d_set, res

