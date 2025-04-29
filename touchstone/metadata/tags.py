# SPDX-FileCopyrightText: 2025 Adam Winick
#
# SPDX-License-Identifier: Apache-2.0

"""Tagging system for categorizing quantum algorithms."""

from enum import Enum
from typing import Callable, TypeVar

# Generic type for classes
T = TypeVar("T", bound=type[object])


class Tag(Enum):
    """
    Enum representing structural and functional tags for quantum algorithms.

    Tags are used to describe input types, construction methods, and output characteristics.
    """

    # Input characteristics
    CLASSICAL_INPUT = "classical_input"
    PARAMETRIC_INPUT = "parametric_input"

    # Algorithm construction
    PARAMETRIC_ALGORITHM = "parametric_algorithm"

    # Output characteristics
    CLASSICAL_OUTPUT = "classical_output"
    KNOWN_DISTRIBUTION = "known_distribution"
    SINGLE_OUTCOME_DISTRIBUTION = "single_outcome_distribution"


def tagged(*tags: Tag) -> Callable[[T], T]:
    """
    Class decorator that attaches static tags to a quantum algorithm class.

    Parameters
    ----------
    *tags : Tag
        One or more Tag enum members to associate with the class.

    Returns
    -------
    Callable[[T], T]
        The original class with an updated `_tags` attribute containing the assigned tags.
    """

    def decorator(cls: T) -> T:
        cls._tags = getattr(cls, "_tags", set()).union(tags)  # type: ignore[attr-defined]
        return cls

    return decorator
