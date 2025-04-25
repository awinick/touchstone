"""
Greenberger-Horne-Zeilinger (GHZ) state preparation algorithm.
"""

from qiskit import QuantumCircuit

from touchstone.algorithms.base_algorithm import BaseAlgorithm, MeasurementMode


class GHZ(BaseAlgorithm):
    """
    Algorithm for preparing a GHZ (Greenberger-Horne-Zeilinger) state.

    Applies a Hadamard gate to the first qubit followed by a chain of CNOT gates to entangle all
    qubits.
    """

    def __init__(self, num_qubits: int):
        """
        Parameters
        ----------
        num_qubits : int
            Number of qubits in the GHZ state.

        Raises
        ------
        ValueError
            If num_qubits is less than 2.
        """
        if num_qubits < 2:
            raise ValueError("Number of qubits must be an integer >= 2.")

        super().__init__("ghz", num_qubits)

    def _build(self, measurement: MeasurementMode) -> QuantumCircuit:
        circuit = QuantumCircuit(self.num_qubits, name=self.name)

        circuit.h(0)

        for i in range(self.num_qubits - 1):
            circuit.cx(i, i + 1)

        if measurement == MeasurementMode.DEFAULT:
            circuit.measure_all()

        return circuit
