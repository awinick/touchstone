# SPDX-FileCopyrightText: 2025 Adam Winick
#
# SPDX-License-Identifier: Apache-2.0

"""
Quantum ripple-carry adder using majority and unmajority gates.

Implements the reversible adder from:
Cuccaro et al., "A new quantum ripple-carry addition circuit", arXiv:quant-ph/0410184.
"""

from qiskit.circuit import ClassicalRegister, Gate, QuantumCircuit, QuantumRegister

from touchstone.algorithms.base_algorithm import BaseAlgorithm


class RippleCarryAdder(BaseAlgorithm):
    """
    Ripple-carry adder using the Cuccaro majority/unmajority construction.

    Computes the sum of two equal-length bitstrings using reversible logic.

    Reference: [Cuccaro et al. (2004)](https://arxiv.org/abs/quant-ph/0410184)
    """

    def __init__(self, augend_bits: str, addend_bits: str) -> None:
        """
        Initialize the ripple-carry adder with two bitstrings.

        Parameters
        ----------
        augend_bits : str
            Bitstring representing the augend (left-hand operand).
        addend_bits : str
            Bitstring representing the addend (right-hand operand).

        Raises
        ------
        ValueError
            If the bitstrings are empty or of unequal length.
        """
        super().__init__("ripple_carry_adder", 2 * len(augend_bits) + 2)

        if not augend_bits or len(augend_bits) != len(addend_bits):
            raise ValueError("Bitstrings must be non-empty and of equal length.")

        self.augend_bits = augend_bits
        self.addend_bits = addend_bits
        self.num_bits = len(augend_bits)

    def _build(self) -> QuantumCircuit:
        carry_in = QuantumRegister(1, "c_in")
        augend = QuantumRegister(self.num_bits, "a")
        addend = QuantumRegister(self.num_bits, "b")
        carry_out = QuantumRegister(1, "c_out")

        circuit = QuantumCircuit(
            carry_in,
            augend,
            addend,
            carry_out,
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
            )

        sum_register = ClassicalRegister(self.num_bits + 1, "sum")
        circuit.add_register(sum_register)
        circuit.barrier()

        # Measure each bit of the sum
        for i in range(self.num_bits):
            circuit.measure(addend[i], sum_register[i])

        # Measure the final carry bit
        circuit.measure(carry_out, sum_register[self.num_bits])

        return circuit

    @property
    def _custom_gates(self) -> list[type[Gate]]:
        """
        List of custom gates used in the algorithm.

        Returns
        -------
        list[Gate]
            List of custom gates.
        """
        return [MajorityGate, UnmajorityGate]


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
