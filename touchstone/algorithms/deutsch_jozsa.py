# SPDX-FileCopyrightText: 2025 Adam Winick
#
# SPDX-License-Identifier: Apache-2.0

"""
Deutsch-Jozsa algorithm.

Identifies if a function is constant or balanced using a single query to an oracle.
"""

from __future__ import annotations

import numpy as np
from qiskit.circuit import AncillaRegister, ClassicalRegister, QuantumCircuit, QuantumRegister

from touchstone.algorithms.base_algorithm import BaseAlgorithm, HasDistribution


class DeutschJozsa(BaseAlgorithm, HasDistribution):
    """
    Deutsch-Jozsa algorithm for determining if a function is constant or balanced.

    This algorithm uses quantum parallelism and interference to determine if a binary-valued
    function is constant (same output for all inputs) or balanced (outputs 0 for half the inputs
    and 1 for the other half), using a single evaluation of a quantum oracle.
    """

    def __init__(self, hidden_string: str):
        """
        Initialize the Deutsch-Jozsa algorithm.

        Parameters
        ----------
        hidden_string : str
            If True, simulate a balanced oracle; otherwise, simulate a constant oracle.

        Raises
        ------
        ValueError
            If the number of qubits is less than 2.
        """
        if len(hidden_string) < 1:
            raise ValueError("Hidden string must be non-empty.")

        super().__init__("deutsch_jozsa", len(hidden_string) + 1)
        self.hidden_string = hidden_string

    @classmethod
    def _from_random(cls, num_qubits: int, rng: np.random.Generator) -> DeutschJozsa:
        hidden_length = num_qubits - 1
        hidden_string = "".join(rng.choice(["0", "1"]) for _ in range(hidden_length))
        return cls(hidden_string)

    @staticmethod
    def _is_num_qubits_valid(num_qubits: int) -> bool:
        return num_qubits >= 2

    def _build(self) -> QuantumCircuit:
        system = QuantumRegister(self.num_qubits - 1, "system")
        ancilla = AncillaRegister(1)
        output = ClassicalRegister(self.num_qubits - 1, "output")

        circuit = QuantumCircuit(system, ancilla, output, name=self.name)

        # Initialize the ancilla qubit
        circuit.x(ancilla)
        circuit.h(ancilla)

        # Apply a Hadamard gate to all system qubits
        circuit.h(system)

        circuit.barrier()

        # Apply the oracle
        for qubit, bit in zip(system, reversed(self.hidden_string)):
            if bit == "1":
                circuit.x(qubit)

            circuit.cx(qubit, ancilla)

            if bit == "1":
                circuit.x(qubit)

        # Apply a Hadamard gate to all system qubits
        circuit.h(system)

        # Measure the system qubits
        circuit.barrier()
        circuit.measure(system, output)

        return circuit

    def distribution(self) -> dict[str, float]:
        """
        Return the distribution of measurement outcomes.

        Returns
        -------
        dict[str, float]
            A dictionary with the expected measurement outcomes and their probabilities.
        """
        return {"1" * (self.num_qubits - 1): 1.0}
