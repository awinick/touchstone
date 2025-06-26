# SPDX-FileCopyrightText: 2025 Adam Winick
#
# SPDX-License-Identifier: Apache-2.0

"""
Grover's search algorithm.

Amplifies the probability of marked basis states using an oracle and diffusion operator.
"""

from __future__ import annotations

from typing import Optional

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import MCXGate

from touchstone.algorithms.base_algorithm import BaseAlgorithm, HasDistribution
from touchstone.metadata.tags import Tag, tagged


@tagged(Tag.CLASSICAL_INPUT, Tag.KNOWN_DISTRIBUTION)
class Grover(BaseAlgorithm, HasDistribution):
    """
    Grover's search algorithm applied to marked state amplification.

    This algorithm amplifies the probability of measuring one or more marked bitstrings in an
    unsorted search space using amplitude amplification. It achieves a quadratic speedup over
    classical search by iteratively applying an oracle and a diffusion operator.

    The oracle flips the phase of marked states, while the diffusion operator inverts amplitudes
    about the average. The number of iterations determines how much amplification occurs.
    """

    def __init__(self, hidden_strings: list[str], iterations: Optional[int] = None) -> None:
        r"""
        Initialize the Grover search instance.

        This constructor accepts a list of marked bitstrings and, optionally, a number of Grover
        iterations. The hidden strings represent states that the oracle marks. If no iteration
        count is provided, the optimal number is computed automatically.

        Parameters
        ----------
        hidden_strings : list[str]
            A list of binary strings representing the marked items.

        iterations : Optional[int]
            Number of Grover iterations to apply. If None, an optimal value is computed as
            $\left\lfloor \frac{\pi}{4} \sqrt{\frac{2^n}{m}} \right\rfloor \,,$
            where $n$ is the number of qubits and $m$ is the number of hidden strings.

        Raises
        ------
        ValueError
            If the list of hidden strings is empty or any string is shorter than 2 bits.
            If not all bitstrings are the same length.
            If half or more of all possible states are marked.
            If a manually specified iteration count is not positive.
        """
        if not hidden_strings:
            raise ValueError("The list of hidden strings must be non-empty.")

        num_qubits = len(hidden_strings[0])

        if num_qubits < 2:
            raise ValueError("Each hidden string must have at least 2 elements.")

        if any(len(hidden_string) != num_qubits for hidden_string in hidden_strings):
            raise ValueError("All hidden strings must have the same length.")

        if len(hidden_strings) >= 2 ** (num_qubits - 1):
            raise ValueError("Grover is illogical when half or more of the states are marked.")

        if iterations is None:
            self.iterations = int(np.pi / 4 * np.sqrt((1 << num_qubits) / len(hidden_strings)))
        elif iterations < 1:
            raise ValueError("Iterations must be positive.")
        else:
            self.iterations = iterations

        self.hidden_strings = hidden_strings

        super().__init__("grover", num_qubits)

    @classmethod
    def _from_random(cls, num_qubits: int, rng: np.random.Generator) -> Grover:
        hidden_strings = ["".join(rng.choice(["0", "1"]) for _ in range(num_qubits))]
        return cls(hidden_strings)

    @staticmethod
    def _is_num_qubits_valid(num_qubits: int) -> bool:
        return num_qubits >= 2

    def _build(self) -> QuantumCircuit:
        # build the oracle
        oracle = QuantumCircuit(self.num_qubits)

        for hidden_string in self.hidden_strings:
            for i, b in enumerate(hidden_string[::-1]):
                if b == "0":
                    oracle.x(i)

            oracle.h(oracle.qubits[-1])
            oracle.append(MCXGate(self.num_qubits - 1), oracle.qubits)
            oracle.h(self.num_qubits - 1)

            for i, b in enumerate(hidden_string[::-1]):
                if b == "0":
                    oracle.x(i)

        # build the diffusion operator
        diffusion = QuantumCircuit(self.num_qubits)

        diffusion.h(diffusion.qubits)
        diffusion.x(diffusion.qubits)

        diffusion.h(diffusion.qubits[-1])
        diffusion.append(MCXGate(self.num_qubits - 1), diffusion.qubits)
        diffusion.h(diffusion.qubits[-1])

        diffusion.x(diffusion.qubits)
        diffusion.h(diffusion.qubits)

        # build the circuit
        circuit = QuantumCircuit(self.num_qubits, name=self.name)
        circuit.h(circuit.qubits)

        for _ in range(self.iterations):
            circuit.compose(oracle, inplace=True)
            circuit.compose(diffusion, inplace=True)

        circuit.measure_all()

        return circuit

    def distribution(self) -> dict[str, float]:
        """
        Return the distribution of measurement outcomes.

        Returns
        -------
        dict[str, float]
            A dictionary with the expected measurement outcomes and their probabilities.
        """
        num_strings = len(self.hidden_strings)
        dimension = 1 << self.num_qubits

        time = np.arcsin(np.sqrt(num_strings / dimension))
        success_probability = np.sin((2 * self.iterations + 1) * time) ** 2
        marginal_success_probability = success_probability / num_strings

        failure_probability = 1 - success_probability
        marginal_failure_probability = failure_probability / (dimension - num_strings)

        result = {
            f"{i:0{self.num_qubits}b}": marginal_failure_probability for i in range(dimension)
        }

        for bitstring in self.hidden_strings:
            result[bitstring] = marginal_success_probability
        return result
