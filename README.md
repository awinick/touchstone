# Touchstone

**touch·stone**
_/ˈtəCHˌstōn/_ • _noun_

> **1.** a standard or criterion by which something is judged or recognized.
>
> **2.** a hard stone used to test the purity of gold or silver by the streak left on its surface.
>
> Touchstone isn’t a transpiler. It’s a measure.
> We give you the stone. You decide what to do with it.

**Touchstone** is a modern library for generating **structured quantum benchmarking circuits** focusing on clarity, composability, and usability.

## Why Touchstone?

Most quantum benchmarking tools today are either overly academic or painfully inflexible. Touchstone is a fresh take on what circuit benchmarking should be:

- **Built for experimentation**, not just file dumping
- **Minimal or highly configurable** — and everything in-between
- **Modular circuit construction** with intuitive tags and filters
- **Ready for real benchmarking** workflows, from transpiler evaluation to device performance tracking

## Example Usage

```python
import touchstone as ts

# Filter the list of algorithms by tags
algorithms = ts.filter_algorithms(ts.Tag.SIMULABLE, ts.Tag.DETERMINISTIC)

# Instantiate circuits within a qubit range
algorithm_instances = ts.instantiate_by(
    algorithms,
    min_qubits = 4,
    max_qubits = 50,
)

# Option 1: Create a dictionary of Qiskit circuits
circuits = ts.build(algorithm_instances)

# Option 2: Save the circuits as QASM
ts.build(algorithm_instances, type=ts.QASM, dir="circuits")
```

## Installation

Touchstone uses [Poetry documentation](https://python-poetry.org/docs/#installation) for dependency management and installation.

### Requirements

- Python 3.11+
- [Poetry installed](https://python-poetry.org/docs/#installation) (recommended)

### Install Touchstone

After installing Poetry, run:

```shell
git clone git@github.com:awinick/touchstone.git
cd touchstone
poetry install
```

This will install Touchstone and all of its dependencies in a clean, managed environment.

### Verify Installation

To run tests and verify the installation:

```shell
poetry run pytest
```
