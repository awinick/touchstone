# SPDX-FileCopyrightText: 2025 Adam Winick
#
# SPDX-License-Identifier: Apache-2.0

"""
Base class for canonical quantum algorithms.

Defines the interface and lifecycle for constructing quantum circuits in a modular and
consistent manner.
"""

from abc import ABC, abstractmethod

from qiskit import QuantumCircuit

from touchstone.metadata.tags import Tag


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
        decompose_custom: bool = True,
    ) -> QuantumCircuit:
        """
        Construct the circuit implementing the algorithm.

        Parameters
        ----------
        decompose_custom : bool
            If True, decomposes the custom gates in the circuit into standard gates.

        Returns
        -------
        QuantumCircuit
            The quantum circuit implementing the algorithm.
        """
        circuit = self._build()

        if decompose_custom and self._custom_gates:
            return circuit.decompose(self._custom_gates)
        return circuit

    @classmethod
    def tags(cls) -> set[Tag]:
        """
        Return the tags associated with the algorithm.

        Tags are used for filtering algorithms based on their properties.

        Returns
        -------
        set[Tag]
            A set of tags associated with the algorithm.
        """
        return getattr(cls, "_tags", set())

    @abstractmethod
    def _build(self) -> QuantumCircuit:
        """
        Construct the circuit implementing the algorithm.

        Subclasses must implement this method to define the algorithm logic.

        Returns
        -------
        QuantumCircuit
            The constructed quantum circuit.
        """

    @property
    def _custom_gates(self) -> list[str]:
        """
        List of custom gates used in the algorithm.

        Returns
        -------
        list[str]
            A list of custom gate names.
        """
        return []


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
