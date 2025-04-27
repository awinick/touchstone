# SPDX-FileCopyrightText: 2025 Adam Winick
#
# SPDX-License-Identifier: Apache-2.0

"""Utility functions."""

import numpy as np
from qiskit.circuit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Statevector

from touchstone.algorithms.base_algorithm import BaseAlgorithm


def simulate_distribution(
    circuit: QuantumCircuit,
    tolerance: float = 1e-10,
) -> dict:
    """
    Simulate the quantum circuit and return the statevector.

    Parameters
    ----------
    circuit : QuantumCircuit
        The quantum circuit to simulate.

    Returns
    -------
    dict
        A dictionary where the keys are bitstrings and the values are the amplitudes.
    """
    initial_state = Statevector.from_int(0, circuit.num_qubits * (2,))
    final_state = initial_state.evolve(circuit)
    raw_distribution = final_state.probabilities_dict()

    return {
        str(bitstring): np.real(amplitude)
        for bitstring, amplitude in raw_distribution.items()
        if np.abs(amplitude) > tolerance
    }


def simulate_counts(
    circuit: QuantumCircuit,
    shots: int = 10,
    seed: np.random.Generator | int | None = 0,
) -> dict:
    """
    Simulate the quantum circuit and return the counts of the measurement results.

    The circuit is executed using a statevector simulator.

    Parameters
    ----------
    circuit : QuantumCircuit
        The quantum circuit to simulate.

    shots : int
        The number of shots (repetitions) for the simulation.

    seed : np.random.Generator | int | None
        Random seed for reproducibility. If None, a random seed is used.
        If an integer is provided, it is used as the seed for the random number generator.

    Returns
    -------
    dict
        A dictionary where the keys are bitstrings and the values are the counts of each bitstring.
    """
    sampler = StatevectorSampler(seed=seed)
    data = sampler.run([circuit], shots=shots).result()[0].data

    if len(data.keys()) != 1:
        raise ValueError("Expected only one result key.")

    return data[list(data.keys())[0]].get_counts()


def normalize_counts(counts: dict[str, int]) -> dict[str, float]:
    """
    Normalize the counts dictionary to convert counts to probabilities.

    Parameters
    ----------
    counts : dict[str, int]
        A dictionary where the keys are bitstrings and the values are the counts.

    Returns
    -------
    dict[str, float]
        A dictionary where the values are the normalized probabilities.
    """
    total = sum(counts.values())
    return {bitstring: count / total for bitstring, count in counts.items()}


def variational_distance(p: dict[str, float], q: dict[str, float]) -> float:
    """
    Calculate the variational distance between two probability distributions.

    Parameters
    ----------
    p : dict[str, float]
        The first probability distribution.

    q : dict[str, float]
        The second probability distribution.

    Returns
    -------
    float
        The variational distance between the two distributions.
    """
    keys = set(p) | set(q)
    return 0.5 * sum(abs(p.get(key, 0) - q.get(key, 0)) for key in keys)


def assert_distributions_close(
    p: dict[str, float],
    q: dict[str, float],
    tolerance: float = 1e-10,
) -> None:
    """
    Assert that two probability distributions are close to each other.

    Parameters
    ----------
    p : dict[str, float]
        The first probability distribution.

    q : dict[str, float]
        The second probability distribution.

    tolerance : float
        The tolerance for closeness.

    Raises
    ------
    AssertionError
        If the variational distance between the two distributions is greater than the tolerance.
    """
    assert variational_distance(p, q) < tolerance


def assert_custom_gate_decomposition(algorithm: BaseAlgorithm) -> None:
    """
    Assert that the custom gates in the algorithm are decomposed.

    Parameters
    ----------
    algorithm : BaseAlgorithm
        The algorithm to check for custom gate decomposition.

    Raises
    ------
    AssertionError
        If the custom gates are not decomposed.
    """
    custom_gate_names = set(algorithm._custom_gates)

    assert len(custom_gate_names)

    op_names = set(algorithm.build(decompose_custom=False).count_ops().keys())
    assert custom_gate_names.issubset(op_names)

    op_names = set(algorithm.build(decompose_custom=True).count_ops().keys())
    assert op_names.isdisjoint(custom_gate_names)
