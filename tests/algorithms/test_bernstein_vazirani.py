"""Unit tests for the Bernstein-Vazirani algorithm."""

import pytest

from tests.utilities import simulate_counts
from touchstone.algorithms.base_algorithm import MeasurementMode
from touchstone.algorithms.bernstein_vazirani import BernsteinVazirani


def test_hidden_string_not_empty() -> None:
    """Test that the hidden string is non-empty."""
    with pytest.raises(ValueError, match="non-empty"):
        BernsteinVazirani("")


def test_measurement_mode() -> None:
    """Test that the circuit has no measurement."""
    hidden_string = "101"
    circuit = BernsteinVazirani(hidden_string).build(measurement=MeasurementMode.NONE)
    assert circuit.count_ops().get("measure", 0) == 0
    circuit = BernsteinVazirani(hidden_string).build(measurement=MeasurementMode.ALL)
    assert circuit.count_ops().get("measure") == 4


@pytest.mark.parametrize(
    "hidden_string",
    [
        "0",
        "1",
        "01",
        "10",
        "11",
        "0000",
        "1111",
        "0101",
        "1010",
        "1100",
    ],
)
def test_circuit_distribution(hidden_string: str) -> None:
    """Test the Bernstein-Vazirani circuit for various hidden strings."""
    algorithm = BernsteinVazirani(hidden_string)
    assert simulate_counts(algorithm.build(), 1) == algorithm.distribution()
