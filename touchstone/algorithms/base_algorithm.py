"""
Base class for canonical quantum algorithms.

Defines the interface and lifecycle for constructing quantum circuits in a modular and
consistent manner.
"""

from abc import ABC, abstractmethod
from enum import Enum

from qiskit.circuit import QuantumCircuit


class MeasurementMode(Enum):
    """
    Modes for applying measurement to a quantum circuit.

    Attributes
    ----------
    NONE : MeasurementMode
        Do not apply any measurements.
    ALL : MeasurementMode
        Measure all qubits in the circuit.
    DEFAULT : MeasurementMode
        Apply algorithm-defined measurements.
    """

    NONE = "none"
    ALL = "measure_all"
    DEFAULT = "default"


class BaseAlgorithm(ABC):
    """
    Abstract base class for quantum algorithm definitions.

    Provides a standardized interface for defining canonical quantum circuits
    used in benchmarking.
    """

    def __init__(self, name: str, num_qubits: int):
        """
        Initialize the algorithm with a name and number of qubits.

        Parameters
        ----------
        name : str
            Name of the algorithm.

        num_qubits : int
            Total number of qubits used.
        """
        self.name = name
        self.num_qubits = num_qubits

    def build(
        self,
        measurement: MeasurementMode = MeasurementMode.DEFAULT,
        decompose_custom: bool = True,
    ) -> QuantumCircuit:
        """
        Construct the circuit implementing the algorithm.

        Parameters
        ----------
        measurement : MeasurementMode
            Controls how measurement operations are applied to the circuit.

        decompose_custom : bool
            If True, decomposes the custom gates in the circuit into standard gates.

        Returns
        -------
        QuantumCircuit
            The quantum circuit implementing the algorithm.
        """
        circuit = self._build(measurement)

        if measurement == MeasurementMode.ALL:
            circuit.measure_all()

        if decompose_custom and hasattr(self, "_custom_gates"):
            return circuit.decompose(self._custom_gates)
        return circuit

    @abstractmethod
    def _build(self, measurement: MeasurementMode) -> QuantumCircuit:
        """
        Construct the core circuit for the algorithm.

        Subclasses must implement this method to define the algorithm logic.
        Measurements should be applied here only if `measurement == DEFAULT`.

        Parameters
        ----------
        measurement : MeasurementMode
            The measurement mode to apply during circuit construction.

        Returns
        -------
        QuantumCircuit
            The constructed quantum circuit.
        """


class HasDistribution(ABC):
    """
    Interface for algorithms with a known measurement outcome distribution.

    Classes implementing this interface must define the expected distribution of
    measurement outcomes as a mapping from bitstrings to probabilities.
    """

    @abstractmethod
    def distribution(self) -> dict[str, float]:
        """
        Return the distribution of measurement outcomes.

        Returns
        -------
        dict[str, float]
            A dictionary with the expected measurement outcomes and their probabilities.
        """
