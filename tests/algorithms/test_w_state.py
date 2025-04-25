"""Unit tests for the W state preparation algorithm."""

import pytest

from tests.utilities import assert_distributions_close, simulate_distribution
from touchstone.algorithms.base_algorithm import MeasurementMode
from touchstone.algorithms.w_state import WState


def test_must_be_greater_than() -> None:
    """Test that the number of qubits is >= 3."""
    with pytest.raises(ValueError, match="integer >= 3"):
        WState(1)


def test_measurement_mode() -> None:
    """Test that the circuit has no measurement."""
    circuit = WState(3).build()
    assert circuit.count_ops().get("measure") == 3


@pytest.mark.parametrize("num_qubits", [3, 4, 5, 6])
def test_circuit_distribution(num_qubits: int) -> None:
    """Test the W State circuit output distribution."""
    algorithm = WState(num_qubits)
    circuit = algorithm.build(measurement=MeasurementMode.NONE)
    assert_distributions_close(simulate_distribution(circuit), algorithm.distribution())
