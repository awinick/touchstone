# SPDX-FileCopyrightText: 2025 Adam Winick
#
# SPDX-License-Identifier: Apache-2.0

"""Unit tests for the W state preparation algorithm."""

import pytest
from qiskit.transpiler.passes import RemoveFinalMeasurements

from tests.utilities import assert_distributions_close, simulate_distribution
from touchstone.algorithms.w_state import WState


def test_must_be_greater_than() -> None:
    """Test that the number of qubits is >= 3."""
    with pytest.raises(ValueError, match="integer >= 3"):
        WState(1)


@pytest.mark.parametrize("num_qubits", [3, 4, 5, 6])
def test_circuit_distribution(num_qubits: int) -> None:
    """Test the W State circuit output distribution."""
    algorithm = WState(num_qubits)
    circuit = RemoveFinalMeasurements()(algorithm.build())
    assert_distributions_close(simulate_distribution(circuit), algorithm.distribution())
