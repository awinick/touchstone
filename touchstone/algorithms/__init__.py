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
from touchstone.algorithms.one_hot_iqft import OneHotIQFT
from touchstone.algorithms.ripple_carry_adder import RippleCarryAdder
from touchstone.algorithms.w_state import WState

__all__ = [
    # Base classes
    "BaseAlgorithm",
    "HasDistribution",
    # Algorithms
    "BernsteinVazirani",
    "GHZ",
    "OneHotIQFT",
    "RippleCarryAdder",
    "WState",
]
