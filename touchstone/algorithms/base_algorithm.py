# SPDX-FileCopyrightText: 2025 Adam Winick
#
# SPDX-License-Identifier: Apache-2.0

"""
Base class for canonical quantum algorithms.

Defines the interface and lifecycle for constructing quantum circuits in a modular and
consistent manner.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Sequence

import numpy as np
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
    def filter_circuit_widths(cls, candidates: Sequence[int]) -> list[int]:
        """
        Filter a sequence of widths to retain only those valid for this algorithm.

        Parameters
        ----------
        candidates : Sequence[int]
            A sequence of candidate circuit widths (number of qubits).

        Returns
        -------
        list[int]
            A list of valid integers from the provided sequence.
        """
        return [q for q in candidates if cls._is_num_qubits_valid(q)]

    @classmethod
    def from_random(
        cls, num_qubits: int, rng: Optional[np.random.Generator] = None
    ) -> BaseAlgorithm:
        """
        Generate a random instance of the algorithm.

        Parameters
        ----------
        num_qubits : int
            Number of qubits for the algorithm. Must be validated externally.

        rng : numpy.random.Generator, optional
            Random number generator for reproducibility. Defaults to numpy's default generator.

        Returns
        -------
        BaseAlgorithm
            A randomly constructed instance of the algorithm.

        Raises
        ------
        ValueError
            If `num_qubits` is invalid.
        """
        if not cls._is_num_qubits_valid(num_qubits):
            raise ValueError(f"Invalid number of qubits {num_qubits} for {cls.__name__}.")

        rng = rng or np.random.default_rng(0)

        return cls._from_random(num_qubits, rng)

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

    @classmethod
    @abstractmethod
    def _from_random(cls, num_qubits: int, rng: np.random.Generator) -> BaseAlgorithm:
        """
        Construct a random instance with reproducible randomized instantiation.

        Parameters
        ----------
        num_qubits : int
            A valid number of qubits for this algorithm.
        rng : np.random.Generator
            A random number generator for reproducibility.

        Returns
        -------
        BaseAlgorithm
            The constructed algorithm instance.

        Notes
        -----
        Subclasses must implement this method to define their randomized construction logic.
        """

    @staticmethod
    @abstractmethod
    def _is_num_qubits_valid(num_qubits: int) -> bool:
        """
        Determine if the given number of qubits is valid for this algorithm.

        Parameters
        ----------
        num_qubits : int
            The number of qubits to validate.

        Returns
        -------
        bool
            True if the number is valid for the algorithm, False otherwise.

        Notes
        -----
        Subclasses must implement this method to define the algorithm logic.
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
