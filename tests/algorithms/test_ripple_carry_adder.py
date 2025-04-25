"""Unit tests for the Ripple-Carry Adder algorithm."""

import pytest

from tests.utilities import simulate_counts
from touchstone.algorithms.base_algorithm import MeasurementMode
from touchstone.algorithms.ripple_carry_adder import RippleCarryAdder


def test_bitstrings_must_not_be_empty() -> None:
    """Test that the bitstrings are non-empty."""
    with pytest.raises(ValueError, match="non-empty"):
        RippleCarryAdder("", "")


def test_bitstrings_must_have_equal_length() -> None:
    """Test that the bitstrings have equal length."""
    with pytest.raises(ValueError, match="equal length"):
        RippleCarryAdder("101", "11")


def test_measurement_mode() -> None:
    """Test that the circuit has no measurement."""
    circuit = RippleCarryAdder("01", "10").build(measurement=MeasurementMode.NONE)
    assert circuit.count_ops().get("measure", 0) == 0


@pytest.mark.parametrize(
    "augend_bits, addend_bits, expected_sum",
    [
        ("00000", "00000", "000000"),
        ("00001", "00001", "000010"),
        ("00001", "00010", "000011"),
        ("00011", "00110", "001001"),
        ("11111", "11111", "111110"),
    ],
)
def test_ripple_carry_adder_circuit(augend_bits: str, addend_bits: str, expected_sum: str) -> None:
    """Test the ripple-carry adder circuit for various bitstrings."""
    shots = 1024
    circuit = RippleCarryAdder(augend_bits, addend_bits).build()
    assert simulate_counts(circuit, shots) == {expected_sum: shots}
