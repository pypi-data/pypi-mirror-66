# Copyright (c) 2020, Xiaotian Derrick Yang
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""Quantum circuit class for containing quantum state."""

import warnings

import numpy as np


class Circuit:
    """Quantum circuit class for containing information for a state."""

    def __init__(self, coeff):
        """Circuit class for storing quantum information.

        Parameters
        ----------
        coeff : np.ndarray(2, ...)
            array of coeffs for each configuration.
            # of dimension matches # of qubits in the system

        Raises
        ------
        ValueError
            Input coeffs is not of proper shape
        """
        # check input type and coeff
        coeff = np.array(coeff, dtype=complex)
        n_qubit = len(coeff.shape)
        for i in range(n_qubit):
            if coeff.shape[i] != 2:
                raise ValueError("Input coeff is not of proper shape.")
        # check input coeff is well normalized
        tot = np.sum(np.abs(coeff) ** 2)
        if abs(tot - 1) > 1e-5:
            warnings.warn(
                "Totel P excess 1., normalization will be applied.", RuntimeWarning
            )
        self._state = coeff / np.sqrt(tot)
        self._nqubit = n_qubit

    @property
    def prob(self):
        """np.ndarray(2, ...): the probability for each configuration."""
        return np.abs(self.state) ** 2

    def measure(self, indices=None):
        """Measure qubits value at given indices.

        Parameters
        ----------
        indices : list of indices, optional
            indices of qubit to perform measurement
            if not given, measure the whole circuit

        Returns
        -------
        tuple(tuple, Circuit)
            the first element is the tuple of measured cubit
            the second element is the leftover cirtuit wavefunction
        """
        # get the indices to sum over prob exclude the selected indices
        if indices is None:
            indices = np.arange(self.n_qubit)
        n_bit = len(indices)
        sum_indices = tuple(set(np.arange(self.n_qubit)).difference(set(indices)))
        # flatten probability into 1d array
        prob = np.sum(self.prob, axis=sum_indices).flatten()
        # get the measure result in the index form and converted to binary
        random_result = np.random.choice(2 ** n_bit, p=prob)
        # convert index into binary result, the same as cubit value
        bin_result = "{:0{}b}".format(random_result, n_bit)
        result = tuple(map(int, bin_result))
        # obtain leftover state for unmeasured cubit(s)
        left_state = np.moveaxis(self._state, indices, list(range(n_bit)))[result]
        # renormalize the probablity distribution
        renorm_state = left_state / np.linalg.norm(left_state)
        return result, Circuit(renorm_state)

    def apply_operator(self, op, indices=[0]):
        """Apply operator on this circuit.

        Parameters
        ----------
        op : Operator
            An operator instance conduting certain operation on circuit
        indices : list, optional
            indices of qubit(s) to perform the operation on.
            if not given, the left-most(index 0) will be selected

        Returns
        -------
        Circuit
            the circuit state after the operation performed

        Raises
        ------
        ValueError
            If the number of selected indices does not match the operator
        """
        n_bit = op.n_target
        if n_bit != len(indices):
            raise ValueError(
                f"# of cubit does not match with the operator.\n"
                f"n_qubit need: {self._nqubit}, got: {len(indices)}"
            )
        # move operated axes to the first n bit
        target_indices = np.arange(n_bit)
        new_state = np.moveaxis(self._state, indices, target_indices)
        # operate with right sequence
        new_state = np.tensordot(
            op.matrix, new_state, axes=[np.arange(-n_bit, 0), target_indices]
        )
        # move operated axes back to original indices
        new_state = np.moveaxis(new_state, target_indices, indices)
        return Circuit(new_state)

    @property
    def n_qubit(self):
        """int: number of qubit in the circuit."""
        return self._nqubit

    @property
    def state(self):
        """np.ndarray(2, ...): state wavefunction of the circuit."""
        return self._state

    def __matmul__(self, other):
        """Implement @ operator for Circuit instance."""
        return Circuit(coeff=np.tensordot(self.state, other.state, axes=0))


def qubit(phi, theta, alpha=0.0):
    """Generate sinle qubit state.

    Parameters
    ----------
    phi : float
        zenith angle on the bloch sphere
    theta : float
        azimuth angle on the bloch sphere
    alpha : float, optional
        Global phace term, default at 0.

    Returns
    -------
    TYPE
        Description
    """
    return Circuit(
        np.exp(alpha * 1j)
        * np.array(
            [np.cos(theta / 2), np.exp(phi * 1j) * np.sin(theta / 2)], dtype=complex,
        )
    )


def bell_state(style=0):
    r"""Generate one of the four bell state for a two-qubit system.

    Parameters
    ----------
    style : int, optional
        0 - 3 is allowed:
        -----------------
        (0)  \phi+ = sqrt(2) (|00> + |11>)
        (1)  \psi+ = sqrt(2) (|01> + |10>)
        (2)  \psi- = sqrt(2) (|00> - |11>)
        (3)  \phi- = sqrt(2) (|00> - |11>)

    Returns
    -------
    Circuit
        Circuit instance with one of the four bell state

    Raises
    ------
    ValueError
        input type value is not between [0, 3]
    """
    if style == 0:
        return Circuit(1 / np.sqrt(2) * np.array([[1, 0], [0, 1]], dtype=complex))
    elif style == 1:
        return Circuit(1 / np.sqrt(2) * np.array([[0, 1], [1, 0]], dtype=complex))
    elif style == 2:
        return Circuit(1 / np.sqrt(2) * np.array([[0, 1], [-1, 0]], dtype=complex))
    elif style == 3:
        return Circuit(1 / np.sqrt(2) * np.array([[1, 0], [0, -1]], dtype=complex))
    else:
        raise ValueError(f"Input style is not a valid value.")
