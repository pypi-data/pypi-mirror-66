# -*- coding: utf-8 -*-
"""
The :mod:`PyDynamic.uncertainty.interpolation` module implements methods for
the propagation of uncertainties in the application of standard interpolation methods
as provided by :class:`scipy.interpolate.interp1d`.

This module contains the following function:

* :func:`interp1d_unc`: Interpolate arbitrary time series considering the associated
  uncertainties
"""

from typing import Optional, Tuple

import numpy as np
from scipy.interpolate import interp1d

__all__ = ["interp1d_unc"]


def interp1d_unc(
    t_new: np.ndarray,
    t: np.ndarray,
    y: np.ndarray,
    uy: np.ndarray,
    kind: Optional[str] = "linear",
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Interpolate arbitrary time series considering the associated uncertainties

    The interpolation timestamps must lie within the range of the original
    timestamps. In addition, at least two of each of the original timestamps,
    measured values and associated measurement uncertainties are required and an
    equal number of each of these three.

    Parameters
    ----------
        t_new: (M,) array_like
            The timestamps at which to evaluate the interpolated values.
        t: (N,) array_like
            timestamps in ascending order
        y: (N,) array_like
            corresponding measurement values
        uy: (N,) array_like
            corresponding measurement values' uncertainties
        kind: str, optional
            Specifies the kind of interpolation for the measurement values
            as a string ('previous', 'next', 'nearest' or 'linear').

    Returns
    -------
        t_new : (M,) array_like
            interpolation timestamps
        y_new : (M,) array_like
            interpolated measurement values
        uy_new : (M,) array_like
            interpolated measurement values' uncertainties

    References
    ----------
        * White [White2017]_
    """
    # Check for ascending order of timestamps.
    if not np.all(t[1:] >= t[:-1]):
        raise ValueError("Array of timestamps needs to be in ascending order.")
    # Check for proper dimensions of inputs.
    if ((t.min() > t_new) | (t.max() < t_new)).any():
        raise ValueError(
            "Array of interpolation timestamps must be in the range of original "
            "timestamps."
        )
    if not len(t) == len(y):
        raise ValueError(
            "Array of measurement values must be same length as array of timestamps."
        )
    if not len(y) == len(uy):
        raise ValueError(
            "Array of associated measurement values' uncertainties must be same length "
            "as array of measurement values."
        )
    # Interpolate measurement values in the desired fashion.
    interp_y = interp1d(t, y, kind=kind)
    y_new = interp_y(t_new)

    if kind in ("previous", "next", "nearest"):
        # Look up uncertainties in cases where it is applicable.
        interp_uy = interp1d(t, uy, kind=kind)
        uy_new = interp_uy(t_new)
    elif kind == "linear":
        # Determine the relevant interpolation intervals for all interpolation
        # timestamps. We determine the intervals for each timestamp in t_new by
        # finding the biggest of all timestamps in t smaller or equal than the one in
        # t_new. From the array of indices of our left interval bounds we get the
        # right bounds by just incrementing the indices, which of course
        # results in index errors at the end of our array, in case the biggest
        # timestamps in t_new are (quasi) equal to the biggest (i.e. last) timestamp
        # in t. This gets corrected just after the iteration by simply manually
        # choosing one interval "further left", which will just at the node result
        # in the same interpolation (being the actual value of y).
        indices = np.empty_like(t_new, dtype=int)
        it_t_new = np.nditer(t_new, flags=["f_index"])
        while not it_t_new.finished:
            # Find indices of biggest of all timestamps smaller or equal
            # than current interpolation timestamp. Assume that timestamps are in
            # ascending order.
            indices[it_t_new.index] = np.where(t <= it_t_new[0])[0][-1]
            it_t_new.iternext()
        # Correct all degenerated intervals. This happens when the last timestamps of
        # t and t_new are equal.
        indices[np.where(indices == len(t) - 1)] -= 1
        t_prev = t[indices]
        t_next = t[indices + 1]
        # Look up corresponding input uncertainties.
        uy_prev_sqr = uy[indices] ** 2
        uy_next_sqr = uy[indices + 1] ** 2
        # Compute uncertainties for interpolated measurement values.
        uy_new = np.sqrt(
            (t_new - t_next) ** 2 * uy_prev_sqr + (t_new - t_prev) ** 2 * uy_next_sqr
        ) / (t_next - t_prev)
    else:
        raise NotImplementedError

    return t_new, y_new, uy_new
