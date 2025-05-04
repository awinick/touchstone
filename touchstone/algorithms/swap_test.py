# SPDX-FileCopyrightText: 2025 Adam Winick
#
# SPDX-License-Identifier: Apache-2.0

"""
Swap test algorithm.

An algorithm used to determine the fidelity between two quantum states.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np
from qiskit.circuit import ClassicalRegister, QuantumCircuit, QuantumRegister

from touchstone.algorithms.base_algorithm import BaseAlgorithm, HasDistribution
from touchstone.metadata.tags import Tag, tagged


@tagged(Tag.PARAMETRIC_INPUT, Tag.KNOWN_DISTRIBUTION)
class SwapTest(BaseAlgorithm, HasDistribution):
    """
    Swap test algorithm for estimating state fidelity.

    This algorithm compares two quantum states by using an ancilla qubit and controlled-SWAP
    operations to estimate their overlap. The probability of measuring the ancilla in the
    |0⟩ state is directly related to the fidelity between the two input states.
    """

    def __init__(self, angles1: Sequence[Sequence[float]], angles2: Sequence[Sequence[float]]):
        """
        Initialize the SwapTest algorithm with two sets of rotation angles.

        Each set of angles defines a parameterized quantum state via U(θ, φ, λ) rotations applied
        to separate registers. The two states are then compared using the swap test.

        Parameters
        ----------
        angles1 : Sequence[Sequence[float]]
            A 2D array of shape (n, 3) representing the Euler angles for the first state.
        angles2 : Sequence[Sequence[float]]
            A 2D array of shape (n, 3) representing the Euler angles for the second state.

        Raises
        ------
        ValueError
            If the angle arrays are not 2D with shape (n, 3) or if their shapes do not match.
        """
        self.angles1 = np.array(angles1)
        self.angles2 = np.array(angles2)

        if self.angles1.shape[0] < 1 or self.angles1.ndim != 2 or self.angles1.shape[1] != 3:
            raise ValueError("Angles must be non-empty 2D arrays with shape (n, 3).")

        if self.angles1.shape != self.angles2.shape:
            raise ValueError("Angles arrays must have the same shape.")

        super().__init__("swap_test", 2 * self.angles1.shape[0] + 1)

    @classmethod
    def _from_random(cls, num_qubits: int, rng: np.random.Generator) -> SwapTest:
        num_state_qubits = (num_qubits - 1) // 2

        angles1 = rng.uniform(0, 2 * np.pi, size=(num_state_qubits, 3)).tolist()
        angles2 = rng.uniform(0, 2 * np.pi, size=(num_state_qubits, 3)).tolist()

        return cls(angles1, angles2)

    @staticmethod
    def _is_num_qubits_valid(num_qubits: int) -> bool:
        return num_qubits % 2 == 1 and num_qubits >= 3

    def _build(self) -> QuantumCircuit:
        state_qubit_count = self.angles1.shape[0]

        test_register = QuantumRegister(1, "test")
        state1_register = QuantumRegister(state_qubit_count, "state1")
        state2_register = QuantumRegister(state_qubit_count, "state2")
        result_register = ClassicalRegister(1, "result")

        circuit = QuantumCircuit(
            test_register,
            state1_register,
            state2_register,
            result_register,
            name=self.name,
        )

        # Prepare the initial states
        for i in range(state_qubit_count):
            circuit.u(*self.angles1[i], state1_register[i])
            circuit.u(*self.angles2[i], state2_register[i])

        circuit.barrier()

        # Apply Hadamard gate to the first qubit
        circuit.h(test_register)

        for i in range(state_qubit_count):
            circuit.cswap(test_register, state1_register[i], state2_register[i])

        # Apply Hadamard gate to the first qubit again
        circuit.h(test_register)

        # Measure the first qubit
        circuit.barrier()
        circuit.measure(test_register, result_register)

        return circuit

    def distribution(self) -> dict[str, float]:
        """
        Return the distribution of measurement outcomes.

        Returns
        -------
        dict[str, float]
            A dictionary with the expected measurement outcomes and their probabilities.
        """
        theta1 = self.angles1[:, 0]
        phi1 = self.angles1[:, 1]
        theta2 = self.angles2[:, 0]
        phi2 = self.angles2[:, 1]

        fidelity = np.prod(
            1
            + np.cos(theta1) * np.cos(theta2)
            + np.cos(phi1 - phi2) * np.sin(theta1) * np.sin(theta2)
        ) / (1 << len(theta1))

        return {
            "0": (1 + fidelity) / 2,
            "1": (1 - fidelity) / 2,
        }
