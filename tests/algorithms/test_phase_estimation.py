# SPDX-FileCopyrightText: 2025 Adam Winick
#
# SPDX-License-Identifier: Apache-2.0

"""Unit tests for the phase estimation algorithm."""

import pytest

from tests.utilities import assert_distributions_close, simulate_distribution
from touchstone.algorithms.phase_estimation import PhaseEstimation


def test_hidden_string_not_empty() -> None:
    """Test that the hidden string is non-empty."""
    with pytest.raises(ValueError, match="non-empty"):
        PhaseEstimation("")


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
    """Test phase estimation for various hidden strings."""
    algorithm = PhaseEstimation(hidden_string)
    assert_distributions_close(simulate_distribution(algorithm.build()), algorithm.distribution())
