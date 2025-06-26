# SPDX-FileCopyrightText: 2025 Adam Winick
#
# SPDX-License-Identifier: Apache-2.0

"""Utility functions."""

from qiskit.circuit import Measure, QuantumCircuit
from qiskit.quantum_info import Statevector

from touchstone.algorithms.base_algorithm import BaseAlgorithm


def simulate_distribution(
    circuit: QuantumCircuit,
    tolerance: float = 1e-10,
) -> dict[str, float]:
    """
    Simulate a quantum circuit and return the marginal output distribution.

    This function removes the measurements from the circuit and simulates
    the circuit to obtain the marginal probability distribution of the
    measured classical bits. The result is a dictionary mapping classical
    bitstrings (as strings) to their corresponding output probabilities.

    Parameters
    ----------
    circuit : QuantumCircuit
        The input quantum circuit containing measurements.
    tolerance : float, optional
        Minimum probability threshold to include in the result.

    Returns
    -------
    dict[str, float]
        A dictionary mapping classical bitstrings (as strings) to their
        corresponding output probabilities.
    """
    # Find measured qubit indices and corresponding classical bit indices
    measurement_mapping = {
        circuit.find_bit(instruction.qubits[0]).index: circuit.find_bit(instruction.clbits[0]).index
        for instruction in circuit.data
        if isinstance(instruction.operation, Measure)
    }

    qubit_index_list = list(measurement_mapping.keys())

    # Remove the measurements from the circuit
    circuit = circuit.remove_final_measurements(inplace=False)

    # Simulate the circuit to get a marginal probability distribution
    marginal_probabilities = Statevector.from_instruction(circuit).probabilities_dict(
        qubit_index_list
    )

    result = {}
    for bitstring, probability in marginal_probabilities.items():
        if probability < tolerance:
            continue

        classical_bits = len(measurement_mapping) * ["0"]

        # Map each measured qubit index to its classical bit index
        for qubit_index, clbit_index in measurement_mapping.items():
            classical_bits[clbit_index] = bitstring[qubit_index_list.index(qubit_index)]

        result["".join(classical_bits)] = probability

    return result


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
