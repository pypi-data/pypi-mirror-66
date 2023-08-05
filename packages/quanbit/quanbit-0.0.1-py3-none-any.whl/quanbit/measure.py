# Copyright (c) 2020, Xiaotian Derrick Yang
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""Measure function of a wavefunction."""


def Measure(Circuit, indices):
    """Measure a Circuit at given indices for its value(s).

    Parameters
    ----------
    Circuit : Circuit
        a Circuit instance
    indices : list or list-like
        indices for measuring the circuit wafefunction

    Returns
    -------
    tuple(tuple, Circuit)
        the first element is the tuple of measured cubit
        the second element is the leftover cirtuit wavefunction
    """
    return Circuit.measure(indices)
