# SPDX-FileCopyrightText: 2025 Adam Winick
#
# SPDX-License-Identifier: Apache-2.0

"""Unit tests for the Bernstein-Vazirani algorithm."""

import pytest

from tests.utilities import simulate_counts
from touchstone.algorithms.bernstein_vazirani import BernsteinVazirani


def test_hidden_string_not_empty() -> None:
    """Test that the hidden string is non-empty."""
    with pytest.raises(ValueError, match="non-empty"):
        BernsteinVazirani("")


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
