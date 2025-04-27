# SPDX-FileCopyrightText: 2025 Adam Winick
#
# SPDX-License-Identifier: Apache-2.0

"""Unit tests for the Ripple-Carry Adder algorithm."""

import pytest

from tests.utilities import assert_custom_gate_decomposition, simulate_counts
from touchstone.algorithms.ripple_carry_adder import RippleCarryAdder


def test_bitstrings_must_not_be_empty() -> None:
    """Test that the bitstrings are non-empty."""
    with pytest.raises(ValueError, match="non-empty"):
        RippleCarryAdder("", "")


def test_bitstrings_must_have_equal_length() -> None:
    """Test that the bitstrings have equal length."""
    with pytest.raises(ValueError, match="equal length"):
        RippleCarryAdder("101", "11")


def test_custom_gate_decomposition() -> None:
    """Test that the custom gates are decomposed."""
    assert_custom_gate_decomposition(RippleCarryAdder("01", "01"))


@pytest.mark.parametrize(
    "augend_bits, addend_bits",
    [
        ("00000", "00000"),
        ("00001", "00001"),
        ("00001", "00010"),
        ("00011", "00110"),
        ("11111", "11111"),
    ],
)
def test_circuit_distribution(augend_bits: str, addend_bits: str) -> None:
    """Test the ripple-carry adder circuit for various bitstrings."""
    algorithm = RippleCarryAdder(augend_bits, addend_bits)
    circuit = algorithm.build()
    assert simulate_counts(circuit, 1) == algorithm.distribution()
