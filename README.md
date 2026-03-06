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

⚠️ Status: Early public release

Touchstone is currently an early-stage project. The API and core library are stable,
but packaging and installation workflows are still being finalized.

For now the recommended way to use Touchstone is installing from source.

## Why Touchstone?

Most quantum benchmarking tools today are either overly academic or painfully inflexible. Touchstone is a fresh take on what circuit benchmarking should be:

- **Built for experimentation**, not just file dumping
- **Minimal or highly configurable** — and everything in-between
- **Modular circuit construction** with intuitive tags and filters
- **Ready for real benchmarking** workflows, from transpiler evaluation to device performance tracking

## Example Usage

Touchstone provides various levels of abstraction for constructing structured benchmarking circuits.

### High level: Prebuilt collections.

At the highest level Touchstone provides various collections of predefined algorithm instances.

```python
import touchstone as ts

# Load the predefined dictionary of small benchmark instances
instances = ts.algorithm_collections.small_algorithms()

# Option 1: Create a dictionary of Qiskit circuits
circuits = ts.build(instances)

# Option 2: Save the circuits as QASM
ts.build(instances, output_format=ts.QASM3, output_directory="circuits")
```

### Medium level: Tag-based filtering and constrained instantiation.

```python
import touchstone as ts

# Filter the list of algorithms by tags
algorithms = ts.filter_algorithms(ts.Tag.SIMULABLE, ts.Tag.DETERMINISTIC)

# Instantiate circuits within a qubit range
instances = ts.instantiate_by(
    algorithms,
    min_qubits = 4,
    max_qubits = 50,
)

# Option 1: Create a dictionary of Qiskit circuits
circuits = ts.build(instances)

# Option 2: Save the circuits as QASM
ts.build(instances, output_format=ts.QASM3, output_directory="circuits")
```

### Low level: Manual algorithm configuration.

At the lowest level...

```python
import touchstone as ts

instances = ts.to_dict([
    ts.algorithms.GHZ(num_qubits=4),
    ts.algorithms.GHZ(num_qubits=8),
    ts.algorithms.RippleCarryAdder(augend_bits="011", addend_bits="101")
])

# Option 1: Create a dictionary of Qiskit circuits
circuits = ts.build(instances)

# Option 2: Save the circuits as QASM
ts.build(instances, output_format=ts.QASM3, output_directory="circuits")
```

## Installation (Recommended)

Touchstone requires **Python 3.11+**.

It can be installed directly via `pip`:

```shell
pip install quantum-touchstone
```

This is the recommended method for most users.

## Build from Source (Developers Only)

Touchstone uses [Poetry](https://python-poetry.org/) for dependency management and installation.

### Requirements

- Python 3.11+
- [Poetry installed](https://python-poetry.org/docs/#installation) (recommended)

### Install Touchstone from source

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

## Contributing

Contributions to Touchstone are welcome!

If you find a bug, have a feature request, or want to add new benchmark algorithms, feel free to open an issue or submit a pull request.

Touchstone prioritizes clarity, reproducibility, and structured development. Please follow the existing code style and testing practices.

## License

Touchstone is licensed under the [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0).

You are free to use, modify, and distribute this software, subject to the terms of the license.
