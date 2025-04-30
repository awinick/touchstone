# SPDX-FileCopyrightText: 2025 Adam Winick
#
# SPDX-License-Identifier: Apache-2.0

"""Unit tests for the swap test algorithm."""

import pytest

from tests.utilities import assert_distributions_close, simulate_distribution
from touchstone.algorithms.swap_test import SwapTest


def test_angles_non_empty() -> None:
    """Test that the angles are non-empty 2D arrays with shape (n, 3)."""
    angles1 = [[0.1, 0.2]]
    angles2 = [[0.7, 0.8, 0.9]]

    with pytest.raises(ValueError, match="non-empty 2D arrays"):
        SwapTest(angles1, angles2)


def test_angles_same_shape() -> None:
    """Test that the angles are non-empty 2D arrays with shape (n, 3)."""
    angles1 = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
    angles2 = [[0.7, 0.8, 0.9]]

    with pytest.raises(ValueError, match="same shape"):
        SwapTest(angles1, angles2)


def test_circuit_distribution() -> None:
    """Test the swap test circuit output distribution."""
    angles1 = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
    angles2 = [[0.7, 0.8, 0.9], [1.0, 1.1, 1.2]]
    algorithm = SwapTest(angles1, angles2)
    assert_distributions_close(simulate_distribution(algorithm.build()), algorithm.distribution())
