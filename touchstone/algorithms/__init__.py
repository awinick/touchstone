# SPDX-FileCopyrightText: 2025 Adam Winick
#
# SPDX-License-Identifier: Apache-2.0

"""
Defines a standard interface and organizational pattern for quantum algorithms.

All algorithms inherit from `BaseAlgorithm`, which provides a uniform interface for circuit
construction, metadata access, and configurable measurement modes.

Algorithms can be filtered, instantiated, and exported using the high-level utilities provided
by the library.
"""

from touchstone.algorithms.base_algorithm import BaseAlgorithm, HasDistribution
from touchstone.algorithms.bernstein_vazirani import BernsteinVazirani
from touchstone.algorithms.ghz import GHZ
from touchstone.algorithms.grover import Grover
from touchstone.algorithms.one_hot_qft import OneHotQFT
from touchstone.algorithms.phase_estimation import PhaseEstimation
from touchstone.algorithms.ripple_carry_adder import RippleCarryAdder
from touchstone.algorithms.swap_test import SwapTest
from touchstone.algorithms.w_state import WState

__all__ = [
    # Base classes
    "BaseAlgorithm",
    "HasDistribution",
    # Algorithms
    "BernsteinVazirani",
    "GHZ",
    "Grover",
    "OneHotQFT",
    "PhaseEstimation",
    "RippleCarryAdder",
    "SwapTest",
    "WState",
]
