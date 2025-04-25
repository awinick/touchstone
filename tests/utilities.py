"""Utility functions."""

import numpy as np
from qiskit.circuit import QuantumCircuit
from qiskit.primitives import StatevectorSampler


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
