# Touchstone vs The World

This page tracks how Touchstone's algorithm and Hamiltonian suite compare against common open-source quantum libraries and industry benchmarking standards.

Use this page to see which structured assets Touchstone provides today, and what areas are still growing.

## QED-C

Last updated: April 27, 2025

The [QC-App-Oriented-Benchmarks](https://github.com/SRI-International/QC-App-Oriented-Benchmarks) project, developed under the Quantum Economic Development Consortium (QED-C), defines a set of application-focused quantum algorithms and benchmark tasks.

| Algorithm              | Covered?                          | Notes                                                                                 |
| :--------------------- | :-------------------------------- | :------------------------------------------------------------------------------------ |
| Amplitude Estimation   | :material-checkbox-blank-outline: |                                                                                       |
| Bernstein-Vazirani     | :material-checkbox-intermediate:  | Touchstone is more configurable.                                                      |
| Deutsch-Jozsa          | :material-checkbox-intermediate:  | Touchstone is more configurable.                                                      |
| Grover                 | :material-checkbox-intermediate:  | Touchstone is more configurable.                                                      |
| Hamiltonian Simulation | :material-checkbox-blank-outline: | Heisenberg model with disordered fields and TFIM, both with open boundary conditions. |
| Hamlib                 | :material-checkbox-blank-outline: | See Hamlib. They only do a tiny subset.                                               |
| HHL                    | :material-checkbox-blank-outline: | [TODO]                                                                                |
| Hidden Shift           | :material-checkbox-blank-outline: | [TODO]                                                                                |
| Hydrogen Lattice       | :material-checkbox-blank-outline: | [TODO]                                                                                |
| Image Reconstruction   | :material-checkbox-blank-outline: | Beyond scope for Touchstone.                                                          |
| Maxcut                 | :material-checkbox-blank-outline: | [TODO]                                                                                |
| Monte-Carlo            | :material-checkbox-blank-outline: | Beyond scope for Touchstone - Application of Amplitude Estimation.                    |
| Phase Estimation       | :material-checkbox-intermediate:  | Touchstone is more configurable.                                                      |
| Shor                   | :material-checkbox-blank-outline: | [TODO]                                                                                |
| VQE                    | :material-checkbox-blank-outline: | [TODO]                                                                                |

## Supermarq

Last updated: April 27, 2025

[Supermarq](https://github.com/Infleqtion/client-superstaq/) is a suite of application-oriented benchmarks used to measure the performance of quantum computing systems.

| Algorithm                 | Covered?                          | Notes                                                                                                            |
| :------------------------ | :-------------------------------- | :--------------------------------------------------------------------------------------------------------------- |
| Bit Code                  | :material-checkbox-blank-outline: | [TODO]                                                                                                           |
| GHZ State                 | :material-checkbox-intermediate:  |                                                                                                                  |
| Hamiltonian Simulation    | :material-checkbox-blank-outline: | 1D TFIM for Molybdenum diselenide.                                                                               |
| Mermin Bell               | :material-checkbox-blank-outline: | Touchstone provides circuits for GHZ state preparation. Mermin operator measurement and scoring is beyond scope. |
| Phase Code                | :material-checkbox-blank-outline: | [TODO]                                                                                                           |
| QAOA Fermionic Swap Proxy | :material-checkbox-blank-outline: | Need to read more. [TODO]                                                                                        |
| QAOA Vanilla Proxy        | :material-checkbox-blank-outline: | MaxCut on a Sherrington-Kirkpatrick (SK) model. [TODO]                                                           |
| VQE Proxy                 | :material-checkbox-blank-outline: | Need to read more. [TODO]                                                                                        |

## Open QBench

Last updated: April 27, 2025

[Open QBench](https://quantum.psnc.pl/openqbench/) provides raw QASM for a restricted set of circuits with a fixed width and depth for each benchmark.

| Algorithm   | Covered?                          | Notes                            |
| :---------- | :-------------------------------- | :------------------------------- |
| Grover      | :material-checkbox-intermediate:  | Touchstone is more configurable. |
| QFT         | :material-checkbox-intermediate:  | Touchstone is more configurable. |
| VQE (UCCSD) | :material-checkbox-blank-outline: | [TODO]                           |
| QAOA (JSSP) | :material-checkbox-blank-outline: | [TODO]                           |
| QSVM        | :material-checkbox-blank-outline: | [TODO]                           |

## QPack

Last updated: April 27, 2025

[QPack](https://github.com/koenmesman/QPack) aims to set the standard for evaluating quantum-hardware and simulators, using meaningful metrics and practical applications.

| Algorithm          | Covered?                          | Notes  |
| :----------------- | :-------------------------------- | :----- |
| Dominating Set     | :material-checkbox-blank-outline: | [TODO] |
| Maxcut             | :material-checkbox-blank-outline: | [TODO] |
| Traveling Salesman | :material-checkbox-blank-outline: | [TODO] |

## MQT Bench

Last updated: April 27, 2025

[MQT Bench](https://github.com/munich-quantum-toolkit/bench) is a quantum circuit benchmark suite with cross-level support, i.e., providing the same benchmark algorithms for different abstraction levels throughout the quantum computing software stack.

| Algorithm                  | Covered?                                 | Notes                                                                           |
| :------------------------- | :--------------------------------------- | :------------------------------------------------------------------------------ |
| Amplitude Estimation       | :material-checkbox-blank-outline:        | [TODO]                                                                          |
| Bernstein-Vazirani         | :material-checkbox-intermediate:         | Touchstone is more configurable.                                                |
| Deutsch-Jozsa              | :material-checkbox-intermediate:         | Touchstone is more configurable.                                                |
| GHZ State                  | :material-checkbox-intermediate:         |                                                                                 |
| Graph State                | :material-checkbox-intermediate-variant: | The benchmark as implemented does nothing.                                      |
| Grover                     | :material-checkbox-intermediate:         | Touchstone is more configurable. MQT only allows searching for the 1...1 state. |
| QAOA                       | :material-checkbox-blank-outline:        | [TODO]                                                                          |
| QFT                        | :material-checkbox-intermediate:         | The benchmark here does not make much sense.                                    |
| QFT (entangled)            | :material-checkbox-intermediate:         | We take a different approach to QFT benchmarking.                               |
| QNN                        | :material-checkbox-blank-outline:        | [TODO]                                                                          |
| Phase Estimation (exact)   | :material-checkbox-intermediate:         | Touchstone is more configurable.                                                |
| Phase Estimation (inexact) | :material-checkbox-blank-outline:        | [TODO]                                                                          |
| Quark Cardinality          | :material-checkbox-blank-outline:        | [TODO]                                                                          |
| Quark Copula               | :material-checkbox-blank-outline:        | [TODO]                                                                          |
| Random Walk                | :material-checkbox-blank-outline:        | [TODO]                                                                          |
| Random Circuit             | :material-checkbox-intermediate-variant: | Not a meaningful algorithmic benchmark.                                         |
| Shor                       | :material-checkbox-blank-outline:        | [TODO]                                                                          |
| VQE Real Amplitude         | :material-checkbox-blank-outline:        | [TODO]                                                                          |
| VQE SU(2)                  | :material-checkbox-blank-outline:        | [TODO]                                                                          |
| VQE Two Local              | :material-checkbox-blank-outline:        | [TODO]                                                                          |
| W State                    | :material-checkbox-intermediate:         |                                                                                 |

## NWQBench

Last updated: April 28, 2025

[NWQBench](https://github.com/pnnl/nwqbench) presents a large corpus of quantum benchmark routine generators, written in Python. These benchmarking schemes generated are compatible with the languages PyQuil, Q#, Qiskit, and Cirq.

| Algorithm          | Covered?                          | Notes                                                                       |
| :----------------- | :-------------------------------- | :-------------------------------------------------------------------------- |
| Adder              | :material-checkbox-intermediate:  | Touchstone is more configurable.                                            |
| Bernstein-Vazirani | :material-checkbox-intermediate:  | Touchstone is more configurable.                                            |
| Binary Welded Tree | :material-checkbox-blank-outline: | [TODO]                                                                      |
| Cat State          | :material-checkbox-intermediate:  | This is identical to GHZ state preparation.                                 |
| CC                 | :material-checkbox-blank-outline: | [TODO] What is this?                                                        |
| GHZ State          | :material-checkbox-intermediate:  | They incorrectly have a Cat state module which yields an identical circuit. |
| Grover             | :material-checkbox-intermediate:  | Touchstone is more configurable.                                            |
| HHL                | :material-checkbox-blank-outline: | [TODO]                                                                      |
| Ising              | :material-checkbox-blank-outline: | [TODO]                                                                      |
| Multiplier         | :material-checkbox-blank-outline: | [TODO]                                                                      |
| Square Root        | :material-checkbox-blank-outline: | [TODO]                                                                      |
| SAT                | :material-checkbox-blank-outline: | [TODO]                                                                      |
| W State            | :material-checkbox-intermediate:  |                                                                             |

Need to finish this table....

## Future Extensions

Thoughts for future: [NWQBench](https://github.com/pnnl/nwqbench/) -> [QASMBench](https://github.com/pnnl/QASMBench)-> [Benchpress](https://github.com/Qiskit/benchpress/tree/main)

HamLib will have some coverage, [Feynman](https://github.com/meamy/feynman) isn't clear what we would cover.... see Benchpress internals.

[QBraid](https://github.com/qBraid/qbraid-algorithms/)

[QCWare](https://forge.qcware.com)

[BACQ](https://arxiv.org/pdf/2403.12205)

[BenchQC](https://arxiv.org/abs/2504.11204)

[TKET Benchmarks](https://github.com/CQCL/tket_benchmarking)
[AppQSim](https://arxiv.org/abs/2503.04298)

[Source](https://arxiv.org/pdf/2503.04905) that lists a bunch of projects like this
