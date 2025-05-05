# SPDX-FileCopyrightText: 2025 Adam Winick
#
# SPDX-License-Identifier: Apache-2.0

"""
Quantum phase estimation algorithm.

Estimates the phase of an eigenvalue of a single qubit unitary operator.
"""

from __future__ import annotations

import numpy as np
from qiskit.circuit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFTGate

from touchstone.algorithms.base_algorithm import BaseAlgorithm, HasDistribution
from touchstone.metadata.tags import Tag, tagged


@tagged(Tag.CLASSICAL_INPUT, Tag.SINGLE_OUTCOME_DISTRIBUTION)
class PhaseEstimation(BaseAlgorithm, HasDistribution):
    """
    Phase estimation algorithm using a single-qubit diagonal unitary.

    This algorithm constructs a fixed-structure quantum phase estimation algorithm targeting a
    known eigenvalue encoded as a binary phase. It benchmarks the core subroutine of quantum
    phase estimation: controlled unitaries and inverse QFT and does not requiring arbitrary
    unitaries or eigenstates.

    The eigenvalue phase is encoded via a single-qubit phase rotation. This allows fully analytic
    reference distributions, while maintaining meaningful structure for backend performance
    evaluation.

    The circuit uses one `target` qubit and a number of `phase` qubits equal to the number of bits
    in the binary string.
    """

    def __init__(self, hidden_string: str):
        """
        Initialize a phase estimation algorithm.

        Parameters
        ----------
        hidden_string : str
            A binary string encoding the target phase `theta` as a binary fraction:
            `theta` = 0.hidden_string.

        Raises
        ------
        ValueError
            If the hidden string is empty.
        """
        if len(hidden_string) <= 0:
            raise ValueError("Hidden string must be non-empty.")

        super().__init__("phase_estimation", len(hidden_string) + 1)
        self.hidden_string = hidden_string

    @classmethod
    def _from_random(cls, num_qubits: int, rng: np.random.Generator) -> PhaseEstimation:
        hidden_string = "".join(rng.choice(["0", "1"]) for _ in range(num_qubits - 1))
        return cls(hidden_string)

    @staticmethod
    def _is_num_qubits_valid(num_qubits: int) -> bool:
        return num_qubits >= 2

    def _build(self) -> QuantumCircuit:
        phase_register = QuantumRegister(self.num_qubits - 1)
        target_register = QuantumRegister(1)
        result_register = ClassicalRegister(self.num_qubits - 1)

        # Convert the hidden string to a binary representation
        theta = sum(int(bit) * 2 ** (-idx - 1) for idx, bit in enumerate(self.hidden_string))

        circuit = QuantumCircuit(phase_register, target_register, result_register)

        circuit.h(phase_register)
        # Initialize the target register to |1>, which is the eigenstate
        circuit.x(target_register)

        for i, qubit in enumerate(phase_register):
            circuit.cp(2 * np.pi * (2**i) * theta, qubit, target_register)
        circuit.append(QFTGate(len(phase_register)).inverse(), phase_register, copy=False)

        circuit.measure(phase_register, result_register)

        return circuit

    def distribution(self) -> dict[str, float]:
        """
        Return the distribution of measurement outcomes.

        Returns
        -------
        dict[str, float]
            A dictionary with the expected measurement outcomes and their probabilities.
        """
        return {self.hidden_string: 1.0}
