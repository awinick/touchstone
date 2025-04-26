"""Greenberger-Horne-Zeilinger (GHZ) state preparation algorithm."""

from qiskit import QuantumCircuit

from touchstone.algorithms.base_algorithm import BaseAlgorithm, HasDistribution


class GHZ(BaseAlgorithm, HasDistribution):
    r"""
    Algorithm for preparing a GHZ (Greenberger-Horne-Zeilinger) state.

    The GHZ state is defined as:

    $$
    \ket{\text{GHZ}} = \frac{1}{\sqrt{2}} \left( \ket{0}^{\otimes n} + \ket{1}^{\otimes n} \right)
    $$

    The state is also known as a **Cat state**, referring to a superposition of macroscopically
    distinct classical states.
    """

    def __init__(self, num_qubits: int):
        """
        Initialize the GHZ state preparation algorithm.

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

    def _build(self) -> QuantumCircuit:
        circuit = QuantumCircuit(self.num_qubits, name=self.name)

        circuit.h(0)

        for i in range(self.num_qubits - 1):
            circuit.cx(i, i + 1)

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
        return {
            "0" * self.num_qubits: 0.5,
            "1" * self.num_qubits: 0.5,
        }
