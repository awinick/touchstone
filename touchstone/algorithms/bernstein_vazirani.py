# SPDX-FileCopyrightText: 2025 Adam Winick
#
# SPDX-License-Identifier: Apache-2.0

"""
Bernstein-Vazirani algorithm.

Identifies a hidden bitstring using a single query to a phase oracle.
"""

from __future__ import annotations

import numpy as np
from qiskit.circuit import QuantumCircuit

from touchstone.algorithms.base_algorithm import BaseAlgorithm, HasDistribution
from touchstone.metadata.tags import Tag, tagged


@tagged(Tag.CLASSICAL_INPUT, Tag.SINGLE_OUTCOME_DISTRIBUTION)
class BernsteinVazirani(BaseAlgorithm, HasDistribution):
    """
    Bernstein-Vazirani algorithm for recovering a hidden bitstring.

    Uses a phase oracle to encode the hidden bitstring into the phase of a uniform superposition,
    followed by a Hadamard transform to reveal the string.
    """

    def __init__(self, hidden_string: str):
        """
        Initialize the Bernstein-Vazirani algorithm with a hidden bitstring.

        Parameters
        ----------
        hidden_string : str
            The hidden bitstring to recover.

        Raises
        ------
        ValueError
            If the hidden string is empty.
        """
        super().__init__("bernstein_vazirani", len(hidden_string) + 1)

        if len(hidden_string) < 1:
            raise ValueError("Hidden string must be non-empty.")

        self.hidden_string = hidden_string

    @classmethod
    def _from_random(cls, num_qubits: int, rng: np.random.Generator) -> BernsteinVazirani:
        hidden_length = num_qubits - 1
        hidden_string = "".join(rng.choice(["0", "1"]) for _ in range(hidden_length))
        return cls(hidden_string)

    @staticmethod
    def _is_num_qubits_valid(num_qubits: int) -> bool:
        return num_qubits >= 2

    def _build(self) -> QuantumCircuit:
        num_system_qubits = self.num_qubits - 1
        circuit = QuantumCircuit(self.num_qubits, num_system_qubits)

        # Put the ancilla qubit in the |1> state
        circuit.h(num_system_qubits)
        circuit.z(num_system_qubits)

        # Apply Hadamard gates to all qubits
        for index in range(num_system_qubits):
            circuit.h(index)

        circuit.barrier()

        # Loop over qubits and apply the oracle
        for index, bit in enumerate(self.hidden_string[::-1]):
            if bit == "0":
                circuit.p(0, index)
            else:
                circuit.cx(index, num_system_qubits)

        # Apply Hadamard gates to all qubits again
        for index in range(num_system_qubits):
            circuit.h(index)

        circuit.barrier()
        circuit.measure(range(num_system_qubits), range(num_system_qubits))

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
