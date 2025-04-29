# SPDX-FileCopyrightText: 2025 Adam Winick
#
# SPDX-License-Identifier: Apache-2.0

"""
One-hot inverse Quantum Fourier Transform (IQFT) state preparation.

Prepares a basis state hidden by global phases and recovers it via inverse QFT,
yielding a deterministic measurement.

Reference: Generalized from standard QFT hidden shift techniques.
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate

from touchstone.algorithms.base_algorithm import BaseAlgorithm, HasDistribution
from touchstone.metadata.tags import Tag, tagged


@tagged(Tag.CLASSICAL_INPUT, Tag.SINGLE_OUTCOME_DISTRIBUTION)
class OneHotIQFT(BaseAlgorithm, HasDistribution):
    """
    One-hot state preparation followed by an inverse QFT.

    Recovers a hidden computational basis state by undoing applied phase rotations using the
    inverse Quantum Fourier Transform.
    """

    def __init__(self, hidden_string: str):
        """
        Initialize the one-hot IQFT algorithm.

        Parameters
        ----------
        hidden_string : str
            Bitstring representing the hidden basis state to recover.

        Raises
        ------
        ValueError
            If the hidden string is empty.
        """
        super().__init__("one_hot_iqft", len(hidden_string))

        if self.num_qubits <= 0:
            raise ValueError("Hidden string must be non-empty.")

        self.hidden_string = hidden_string

    def _build(self) -> QuantumCircuit:
        circuit = QuantumCircuit(self.num_qubits, name="one_hot_iqft")

        hidden_int = int(self.hidden_string, 2)
        for qubit in range(self.num_qubits):
            circuit.h(qubit)
            circuit.p(hidden_int * np.pi / 2 ** (self.num_qubits - qubit - 1), qubit)

        circuit.barrier()

        circuit.compose(QFTGate(self.num_qubits).inverse(), inplace=True, copy=False)

        circuit.measure_all()

        return circuit

    @property
    def _custom_gates(self) -> list[str]:
        """
        List of custom gates used in the algorithm.

        Returns
        -------
        list[str]
            A list of custom gate names.
        """
        return ["qft_dg"]

    def distribution(self) -> dict[str, float]:
        """
        Return the distribution of measurement outcomes.

        Returns
        -------
        dict[str, float]
            A dictionary with the expected measurement outcomes and their probabilities.
        """
        return {self.hidden_string: 1.0}
