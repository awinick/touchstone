# SPDX-FileCopyrightText: 2025 Adam Winick
#
# SPDX-License-Identifier: Apache-2.0

"""
Bernstein-Vazirani algorithm.

Identifies a hidden bitstring using a single query to a phase oracle.
"""

from qiskit.circuit import QuantumCircuit

from touchstone.algorithms.base_algorithm import BaseAlgorithm, HasDistribution


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
        super().__init__("bernstein_vazirani", len(hidden_string))

        if self.num_qubits <= 0:
            raise ValueError("Hidden string must be non-empty.")

        self.hidden_string = hidden_string

    def _build(self) -> QuantumCircuit:
        circuit = QuantumCircuit(self.num_qubits + 1, self.num_qubits)

        # Put the ancilla qubit in the |1> state
        circuit.h(self.num_qubits)
        circuit.z(self.num_qubits)

        # Apply Hadamard gates to all qubits
        for index in range(self.num_qubits):
            circuit.h(index)

        # Loop over qubits and apply the oracle
        for index, bit in enumerate(self.hidden_string[::-1]):
            if bit == "0":
                circuit.p(0, index)
            else:
                circuit.cx(index, self.num_qubits)

        # Apply Hadamard gates to all qubits again
        for index in range(self.num_qubits):
            circuit.h(index)

        circuit.barrier(self.num_qubits)
        circuit.measure(range(self.num_qubits), range(self.num_qubits))

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
