"""
This module defines a standard interface and organizational pattern for quantum algorithms,
focusing on composability, instantiation control, and tagging.

All algorithms inherit from `BaseAlgorithm`, which provides a uniform interface for circuit
construction, metadata access, and configurable measurement modes.

Algorithms can be filtered, instantiated, and exported using the high-level utilities provided by the library.
"""

from .base_algorithm import BaseAlgorithm, MeasurementMode
from .bernstein_vazirani import BernsteinVazirani
from .ghz import GHZ
from .ripple_carry_adder import RippleCarryAdder
from .w_state import WState

__all__ = [
    "BaseAlgorithm",
    "MeasurementMode",
    "BernsteinVazirani",
    "GHZ",
    "RippleCarryAdder",
    "WState",
]
