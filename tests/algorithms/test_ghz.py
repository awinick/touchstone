# SPDX-FileCopyrightText: 2025 Adam Winick
#
# SPDX-License-Identifier: Apache-2.0

"""Unit tests for the GHZ state preparation algorithm."""

import pytest

from tests.utilities import assert_distributions_close, simulate_distribution
from touchstone.algorithms.ghz import GHZ


def test_must_be_greater_than() -> None:
    """Test that the number of qubits is >= 2."""
    with pytest.raises(ValueError, match="integer >= 2"):
        GHZ(1)


@pytest.mark.parametrize("num_qubits", [2, 3, 4])
def test_circuit_distribution(num_qubits: int) -> None:
    """Test the GHZ circuit output distribution."""
    algorithm = GHZ(num_qubits)
    assert_distributions_close(simulate_distribution(algorithm.build()), algorithm.distribution())
