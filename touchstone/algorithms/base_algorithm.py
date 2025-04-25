"""Base class for quantum algorithms."""

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
    Abstract base class for canonical quantum algorithms.

    Provides a standard interface for building algorithms and their associated circuits.
    """

    def __init__(self, name: str, num_qubits: int):
        """
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
        decompose: bool = True,
    ) -> QuantumCircuit:
        """
        Construct the circuit implementing the algorithm.

        Parameters
        ----------
        measurement : MeasurementMode
            Controls how measurement operations are applied to the circuit.
        decompose : bool
            If `decompose` is True, the circuit will be decomposed into standard gates.

        Returns
        -------
        QuantumCircuit
            The quantum circuit implementing the algorithm.
        """
        circuit = self._build(measurement)

        if measurement == MeasurementMode.ALL:
            circuit.measure_all()

        return circuit.decompose() if decompose else circuit

    @abstractmethod
    def _build(self, measurement: MeasurementMode) -> QuantumCircuit:
        """
        Constructs the core quantum circuit.

        This method defines the algorithm and may apply measurement if the mode is set to DEFAULT.

        Parameters
        ----------
        measurement : MeasurementMode
            The measurement mode to apply during circuit construction.

        Returns
        -------
        QuantumCircuit
            The constructed quantum circuit.
        """
