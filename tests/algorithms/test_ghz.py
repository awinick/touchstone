"""Unit tests for the GHZ state preparation algorithm."""

import pytest

from tests.utilities import assert_distributions_close, simulate_distribution
from touchstone.algorithms.base_algorithm import MeasurementMode
from touchstone.algorithms.ghz import GHZ


def test_must_be_greater_than() -> None:
    """Test that the number of qubits is >= 2."""
    with pytest.raises(ValueError, match="integer >= 2"):
        GHZ(1)


def test_measurement_mode() -> None:
    """Test that the circuit has no measurement."""
    circuit = GHZ(3).build()
    assert circuit.count_ops().get("measure") == 3


@pytest.mark.parametrize("num_qubits", [2, 3, 4])
def test_circuit_distribution(num_qubits: int) -> None:
    """Test the GHZ circuit output distribution."""
    algorithm = GHZ(num_qubits)
    circuit = algorithm.build(measurement=MeasurementMode.NONE)
    assert_distributions_close(simulate_distribution(circuit), algorithm.distribution())
