# SPDX-FileCopyrightText: 2025 Adam Winick
#
# SPDX-License-Identifier: Apache-2.0

"""
One-hot Quantum Fourier Transform (QFT) state preparation.

Prepares the inverse-QFT state corresponding to a hidden basis bitstring,
which is recovered deterministically by applying a forward QFT.
"""

from __future__ import annotations

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate

from touchstone.algorithms.base_algorithm import BaseAlgorithm, HasDistribution
from touchstone.metadata.tags import Tag, tagged


@tagged(Tag.CLASSICAL_INPUT, Tag.SINGLE_OUTCOME_DISTRIBUTION)
class OneHotQFT(BaseAlgorithm, HasDistribution):
    """
    One-hot basis state preparation followed by a QFT.

    Prepares the QFT encoding of a known classical bitstring, such that a forward QFT transforms
    it into a deterministic computational basis state.
    """

    def __init__(self, hidden_string: str):
        """
        Initialize the one-hot QFT algorithm.

        Parameters
        ----------
        hidden_string : str
            Bitstring representing the hidden basis state to recover.

        Raises
        ------
        ValueError
            If the hidden string is empty.
        """
        super().__init__("one_hot_qft", len(hidden_string))

        if self.num_qubits <= 0:
            raise ValueError("Hidden string must be non-empty.")

        self.hidden_string = hidden_string

    @classmethod
    def _from_random(cls, num_qubits: int, rng: np.random.Generator) -> OneHotQFT:
        hidden_string = "".join(rng.choice(["0", "1"]) for _ in range(num_qubits))
        return cls(hidden_string)

    @staticmethod
    def _is_num_qubits_valid(num_qubits: int) -> bool:
        return num_qubits >= 1

    def _build(self) -> QuantumCircuit:
        circuit = QuantumCircuit(self.num_qubits, name=self.name)

        hidden_int = int(self.hidden_string, 2)
        for qubit in range(self.num_qubits):
            circuit.h(qubit)
            circuit.p(-hidden_int * np.pi / 2 ** (self.num_qubits - qubit - 1), qubit)

        circuit.barrier()

        circuit.compose(QFTGate(self.num_qubits), inplace=True, copy=False)

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
        return ["qft"]

    def distribution(self) -> dict[str, float]:
        """
        Return the distribution of measurement outcomes.

        Returns
        -------
        dict[str, float]
            A dictionary with the expected measurement outcomes and their probabilities.
        """
        return {self.hidden_string: 1.0}
