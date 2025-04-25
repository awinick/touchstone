"""
W state preparation algorithm.
"""

import numpy as np
from qiskit import QuantumCircuit

from touchstone.algorithms.base_algorithm import BaseAlgorithm, MeasurementMode


class WState(BaseAlgorithm):
    r"""
    Algorithm for preparing a W state.

    The W state is a superposition of all basis states with Hamming weight one and is defined as:

    $$
    \ket{\text{W}} = \frac{1}{\sqrt{n}}
    (\ket{100\dots 0} + \ket{010\dots 0} + \cdots + \ket{000\dots 1})
    $$

    It is robust against qubit loss and represents a distinct class of entanglement.
    """

    def __init__(self, num_qubits: int):
        """
        Parameters
        ----------
        num_qubits : int
            Number of qubits in the W state.

        Raises
        ------
        ValueError
            If num_qubits is less than 3.
        """
        if num_qubits < 3:
            raise ValueError("Number of qubits must be an integer >= 3.")

        super().__init__("w_state", num_qubits)

    def _build(self, measurement: MeasurementMode) -> QuantumCircuit:
        circuit = QuantumCircuit(self.num_qubits, name=self.name)

        # Flip the first qubit
        circuit.x(0)

        # Forward amplitude redistribution with RY and CZ gates
        for i in range(1, self.num_qubits):
            theta = np.arccos(np.sqrt(1 / (self.num_qubits - i + 1)))
            circuit.ry(-theta, i)
            circuit.cz(i - 1, i)
            circuit.ry(theta, i)

        # Backwards entanglement with CX gates
        for i in range(self.num_qubits - 1):
            circuit.cx(i + 1, i)

        if measurement == MeasurementMode.DEFAULT:
            circuit.measure_all()

        return circuit
