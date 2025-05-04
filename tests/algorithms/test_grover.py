# SPDX-FileCopyrightText: 2025 Adam Winick
#
# SPDX-License-Identifier: Apache-2.0

"""Unit tests for Grover's algorithm."""

import pytest

from tests.utilities import assert_distributions_close, simulate_distribution
from touchstone.algorithms.grover import Grover


def test_bitstrings_not_empty() -> None:
    """Test that the bitstrings are non-empty."""
    with pytest.raises(ValueError, match="non-empty"):
        Grover([])


def test_bitstrings_minimum_length() -> None:
    """Test that the bitstrings have a minimum length."""
    with pytest.raises(ValueError, match="at least 2 elements"):
        Grover(["0", "1"])


def test_bitstrings_same_length() -> None:
    """Test that the bitstrings have the same length."""
    with pytest.raises(ValueError, match="same length"):
        Grover(["01", "101"])


def test_too_many_bitstrings() -> None:
    """Test that the number of bitstrings is less than half the total number of states."""
    with pytest.raises(ValueError, match="half or more of the states"):
        Grover(["01", "10"])


def test_iterations_positive() -> None:
    """Test that the number of iterations is positive."""
    with pytest.raises(ValueError, match="positive"):
        Grover(["01"], iterations=-1)


def test_iterations_default() -> None:
    """Test that the default number of iterations is set correctly."""
    hidden_string = "011"

    algorithm = Grover([hidden_string])
    assert algorithm.iterations == 2

    optimal_distribution = algorithm.distribution()
    suboptimal_distribution1 = Grover([hidden_string], iterations=1).distribution()
    suboptimal_distribution2 = Grover([hidden_string], iterations=3).distribution()

    assert optimal_distribution[hidden_string] > suboptimal_distribution1[hidden_string]
    assert optimal_distribution[hidden_string] > suboptimal_distribution2[hidden_string]


@pytest.mark.parametrize(
    "hidden_strings",
    [["01"], ["10"], ["11"], ["0000", "0100"], ["1111"], ["0101", "1010", "1100"]],
)
def test_circuit_distribution(hidden_strings: list[str]) -> None:
    """Test the Grover circuit for various hidden strings."""
    algorithm = Grover(hidden_strings)
    assert_distributions_close(simulate_distribution(algorithm.build()), algorithm.distribution())
