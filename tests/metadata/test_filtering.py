# SPDX-FileCopyrightText: 2025 Adam Winick
#
# SPDX-License-Identifier: Apache-2.0

"""Unit tests for algorithm filtering functionality."""

import pytest

from touchstone.algorithms.base_algorithm import BaseAlgorithm
from touchstone.metadata.fitering import filter_algorithms, instantiate_by
from touchstone.metadata.tags import Tag


def test_filter_contradictory_tags() -> None:
    """Test that filtering with contradictory tags raises a ValueError."""
    with pytest.raises(ValueError, match="include and exclude"):
        filter_algorithms(include=[Tag.KNOWN_DISTRIBUTION], exclude=[Tag.KNOWN_DISTRIBUTION])


def test_filter_no_tags() -> None:
    """Test that filtering with no tags returns all algorithms."""
    algorithms = filter_algorithms()
    assert len(algorithms) > 0
    assert all(issubclass(algorithm, BaseAlgorithm) for algorithm in algorithms)


def test_instantiate_by() -> None:
    """Test that instantiate_by returns the correct algorithm class."""
    all_algorithms = filter_algorithms()

    for algorithm in all_algorithms:
        instantiate_by(algorithm, min_qubits=2, max_qubits=5)
