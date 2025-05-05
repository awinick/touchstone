# SPDX-FileCopyrightText: 2025 Adam Winick
#
# SPDX-License-Identifier: Apache-2.0

"""Filtering quantum algorithms based on metadata."""

from typing import Optional, Sequence, cast

from touchstone.algorithms.base_algorithm import BaseAlgorithm
from touchstone.metadata.tags import Tag


def filter_algorithms(
    include: Optional[set | Sequence[Tag]] = None,
    exclude: Optional[set | Sequence[Tag]] = None,
) -> list[type[BaseAlgorithm]]:
    """
    Filter algorithms based on their tags.

    Parameters
    ----------
    include : Optional[Sequence[Tag]]
        A sequence of tags to include in the filter. If `None`, all algorithms are included.
    exclude : Optional[Sequence[Tag]]
        A sequence of tags to exclude from the filter. If `None`, no algorithms are excluded.

    Returns
    -------
    list[type[BaseAlgorithm]]
        A list of algorithm classes that match the specified tags.

    Raises
    ------
    ValueError
        If a tag in `include` is also present in `exclude`.
    """
    include_set = set(include) if include else set()
    exclude_set = set(exclude) if exclude else set()

    if not include_set.isdisjoint(exclude_set):
        raise ValueError("A tag cannot be present in both include and exclude.")

    return [
        cast(type[BaseAlgorithm], algorithm_cls)
        for algorithm_cls in BaseAlgorithm.__subclasses__()
        if include_set.issubset(algorithm_cls.tags())
        and exclude_set.isdisjoint(algorithm_cls.tags())
    ]


def instantiate_by(
    algorithm_class: type[BaseAlgorithm],
    min_qubits: int = 2,
    max_qubits: int = 20,
) -> dict[int, BaseAlgorithm]:
    """
    Instantiate a dictionary of algorithms with random construction.

    Parameters
    ----------
    algorithm_class : type[BaseAlgorithm]
        The class of the algorithm to instantiate.
    min_qubits : int
        The minimum number of qubits for the algorithm.
    max_qubits : int
        The maximum number of qubits for the algorithm.

    Returns
    -------
    dict[str, BaseAlgorithm]
        A dictionary mapping the number of qubits to the instantiated algorithm.
    """
    valid_widths = algorithm_class.filter_circuit_widths(list(range(min_qubits, max_qubits + 1)))
    return {width: algorithm_class.from_random(width) for width in valid_widths}
