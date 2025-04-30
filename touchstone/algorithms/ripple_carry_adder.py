# SPDX-FileCopyrightText: 2025 Adam Winick
#
# SPDX-License-Identifier: Apache-2.0

"""
Quantum ripple-carry adder using majority and unmajority gates.

Implements the reversible adder from:
Cuccaro et al., "A new quantum ripple-carry addition circuit", arXiv:quant-ph/0410184.
"""

from qiskit.circuit import ClassicalRegister, Gate, QuantumCircuit, QuantumRegister

from touchstone.algorithms.base_algorithm import BaseAlgorithm, HasDistribution
from touchstone.metadata.tags import Tag, tagged


@tagged(Tag.CLASSICAL_INPUT, Tag.SINGLE_OUTCOME_DISTRIBUTION)
class RippleCarryAdder(BaseAlgorithm, HasDistribution):
    """
    Ripple-carry adder using the Cuccaro majority/unmajority construction.

    Computes the sum of two equal-length bitstrings using reversible logic.

    Reference: [Cuccaro et al. (2004)](https://arxiv.org/abs/quant-ph/0410184)
    """

    def __init__(self, augend_string: str, addend_string: str) -> None:
        """
        Initialize the ripple-carry adder with two bitstrings.

        Parameters
        ----------
        augend_string : str
            Bitstring representing the augend (left-hand operand).
        addend_string : str
            Bitstring representing the addend (right-hand operand).

        Raises
        ------
        ValueError
            If the bitstrings are empty or of unequal length.
        """
        super().__init__("ripple_carry_adder", 2 * len(augend_string) + 2)

        if not augend_string or len(augend_string) != len(addend_string):
            raise ValueError("Bitstrings must be non-empty and of equal length.")

        self.augend_bits = augend_string
        self.addend_bits = addend_string
        self.num_bits = len(augend_string)

    def _build(self) -> QuantumCircuit:
        carry_in = QuantumRegister(1, "c_in")
        augend = QuantumRegister(self.num_bits, "a")
        addend = QuantumRegister(self.num_bits, "b")
        carry_out = QuantumRegister(1, "c_out")
        result = ClassicalRegister(self.num_bits + 1, "result")

        circuit = QuantumCircuit(
            carry_in,
            augend,
            addend,
            carry_out,
            result,
            name=self.name,
        )

        # Initialize the input registers with the bit strings
        apply_bitstring_to_circuit(circuit, augend, self.augend_bits[::-1])
        apply_bitstring_to_circuit(circuit, addend, self.addend_bits[::-1])

        circuit.barrier()

        # Forward pass: compute carries using majority gates
        for i in range(self.num_bits):
            circuit.append(
                MajorityGate(),
                (
                    augend[i - 1] if i else carry_in,
                    addend[i],
                    augend[i],
                ),
                copy=False,
            )

        # Copy final carry bit into carry_out using CNOT
        circuit.cx(augend[self.num_bits - 1], carry_out)

        # Backward pass: uncompute carries using unmajority gates
        for i in range(self.num_bits - 1, -1, -1):
            circuit.append(
                UnmajorityGate(),
                (
                    augend[i - 1] if i else carry_in,
                    addend[i],
                    augend[i],
                ),
                copy=False,
            )

        # Measure the result
        circuit.barrier()
        for i in range(self.num_bits):
            circuit.measure(addend[i], result[i])
        # Measure the final carry bit
        circuit.measure(carry_out, result[self.num_bits])

        return circuit

    def distribution(self) -> dict[str, float]:
        """
        Return the distribution of measurement outcomes.

        Returns
        -------
        dict[str, float]
            A dictionary with the expected measurement outcomes and their probabilities.
        """
        result = bin(int(self.augend_bits, 2) + int(self.addend_bits, 2))[2:]
        padded_result = result.zfill(self.num_bits + 1)
        return {padded_result: 1.0}

    @property
    def _custom_gates(self) -> list[str]:
        """
        List of custom gates used in the algorithm.

        Returns
        -------
        list[str]
            A list of custom gate names.
        """
        return [MajorityGate().name, UnmajorityGate().name]


class MajorityGate(Gate):
    """Majority gate used to compute carry bits in ripple-carry addition."""

    def __init__(self) -> None:
        """Initialize a 3-qubit majority gate."""
        super().__init__("majority", 3, [])

    def _define(self) -> None:
        circuit = QuantumCircuit(3, name=self.name)
        circuit.cx(2, 1)
        circuit.cx(2, 0)
        circuit.ccx(0, 1, 2)

        self.definition = circuit


class UnmajorityGate(Gate):
    """Unmajority gate used to uncompute carry bits in ripple-carry addition."""

    def __init__(self) -> None:
        """Initialize a 3-qubit unmajority gate."""
        super().__init__("unmajority", 3, [])

    def _define(self) -> None:
        circuit = QuantumCircuit(3, name=self.name)
        circuit.ccx(0, 1, 2)
        circuit.cx(2, 0)
        circuit.cx(0, 1)

        self.definition = circuit


def apply_bitstring_to_circuit(
    circuit: QuantumCircuit, register: QuantumRegister, bitstring: str
) -> None:
    """
    Apply a bitstring to a quantum register by flipping the qubits corresponding to '1's.

    Parameters
    ----------
    circuit : QuantumCircuit
        The quantum circuit to which the bitstring will be applied.
    register : QuantumRegister
        The quantum register to which the bitstring will be applied.
    bitstring : str
        The bitstring to be applied, consisting of '0's and '1's.
    """
    for i, bit in enumerate(bitstring):
        if bit == "1":
            circuit.x(register[i])
