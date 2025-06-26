# SPDX-FileCopyrightText: 2025 Adam Winick
#
# SPDX-License-Identifier: Apache-2.0

"""Unit tests for the Deutsch-Jozsa algorithm."""


import pytest

from tests.utilities import assert_distributions_close, simulate_distribution
from touchstone.algorithms.deutsch_jozsa import DeutschJozsa


def test_hidden_string_not_empty() -> None:
    """Test that the hidden string is non-empty."""
    with pytest.raises(ValueError, match="non-empty"):
        DeutschJozsa("")


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
    ],
)
def test_circuit_distribution(hidden_string: str) -> None:
    """Test the Deutsch-Jozsa circuit for various hidden strings."""
    algorithm = DeutschJozsa(hidden_string)
    assert_distributions_close(simulate_distribution(algorithm.build()), algorithm.distribution())
