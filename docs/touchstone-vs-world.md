# Touchstone vs The World

This page tracks how Touchstone's algorithm and Hamiltonian suite compare against common open-source quantum libraries and industry benchmarking standards.

Use this page to see which structured assets Touchstone provides today, and what areas are still growing.

## QED-C

Last updated: April 27, 2025

The [QC-App-Oriented-Benchmarks](https://github.com/SRI-International/QC-App-Oriented-Benchmarks) project, developed under the Quantum Economic Development Consortium (QED-C), defines a set of application-focused quantum algorithms and benchmark tasks.

| Algorithm              | Covered? | Notes                                                                                                                                 |
| :--------------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------ |
| Amplitude Estimation   | [x]      | Touchstone is more configurable.                                                                                                      |
| Bernstein-Vazirani     | [x]      | Touchstone is more configurable.                                                                                                      |
| Deutsch-Jozsa          | [ ]      | [TODO]                                                                                                                                |
| Grover                 | [x]      | Touchstone is more configurable.                                                                                                      |
| Hamiltonian Simulation | [ ]      | They just do Heisenberg model with disordered fields and the Transverse Field Ising Model (TFIM), both with open boundary conditions. |
| Hamlib                 | [ ]      | See Hamlib. They only do a tiny subset.                                                                                               |
| HHL                    | [ ]      | [TODO]                                                                                                                                |
| Hidden Shift           | [ ]      | [TODO]                                                                                                                                |
| Hydrogen Lattice       | [ ]      | [TODO]                                                                                                                                |
| Image Reconstruction   | [ ]      | Beyond scope for Touchstone.                                                                                                          |
| Maxcut                 | [ ]      | [TODO]                                                                                                                                |
| Monte-Carlo            | [ ]      | Beyond scope for Touchstone - Application of Amplitude Estimation.                                                                    |
| Phase Estimation       | [ ]      | [TODO]                                                                                                                                |
| Shor                   | [ ]      | [TODO]                                                                                                                                |
| VQE                    | [ ]      | [TODO]                                                                                                                                |

## Supermarq

Last updated: April 27, 2025

[Supermarq](https://github.com/Infleqtion/client-superstaq/) is a suite of application-oriented benchmarks used to measure the performance of quantum computing systems.

| Algorithm                 | Covered? | Notes                                                                                                                                     |
| :------------------------ | :------- | :---------------------------------------------------------------------------------------------------------------------------------------- |
| Bit Code                  | [ ]      | [TODO]                                                                                                                                    |
| GHZ State                 | [x]      |                                                                                                                                           |
| Hamiltonian Simulation    | [ ]      | 1D TFIM for Molybdenum diselenide.                                                                                                        |
| Mermin Bell               | [-]      | Touchstone provides circuits for GHZ state preparation. Support for simultaneous Mermin operator measurement and scoring is beyond scope. |
| Phase Code                | [ ]      | [TODO]                                                                                                                                    |
| QAOA Fermionic Swap Proxy | [ ]      | Need to read more. [TODO]                                                                                                                 |
| QAOA Vanilla Proxy        | [ ]      | MaxCut on a Sherrington-Kirkpatrick (SK) model. [TODO]                                                                                    |
| VQE Proxy                 | [ ]      | Need to read more. [TODO]                                                                                                                 |

## Open QBench

Last updated: April 27, 2025

[Open QBench](https://quantum.psnc.pl/openqbench/) provides raw QASM for a restricted set of circuits with a fixed width and depth for each benchmark.

| Algorithm   | Covered? | Notes                            |
| :---------- | :------- | :------------------------------- |
| Grover      | [x]      | Touchstone is more configurable. |
| QFT         | [x]      | Touchstone is more configurable. |
| VQE (UCCSD) | [ ]      | [TODO]                           |
| QAOA (JSSP) | [ ]      | [TODO]                           |
| QSVM        | [ ]      | [TODO]                           |

## QPack

Last updated: April 27, 2025

[QPack](https://github.com/koenmesman/QPack) aims to set the standard for evaluating quantum-hardware and simulators, using meaningful metrics and practical applications.

| Algorithm          | Covered? | Notes  |
| :----------------- | :------- | :----- |
| Dominating Set     | [ ]      | [TODO] |
| Maxcut             | [ ]      | [TODO] |
| Traveling Salesman | [ ]      | [TODO] |

## MQT Bench

Last updated: April 27, 2025

[MQT Bench](https://github.com/munich-quantum-toolkit/bench) is a quantum circuit benchmark suite with cross-level support, i.e., providing the same benchmark algorithms for different abstraction levels throughout the quantum computing software stack.

| Algorithm                  | Covered? | Notes                                                                           |
| :------------------------- | :------- | :------------------------------------------------------------------------------ |
| Amplitude Estimation       | [ ]      | [TODO]                                                                          |
| Bernstein-Vazirani         | [x]      | Touchstone is more configurable.                                                |
| Deutsch-Jozsa              | [ ]      | [TODO]                                                                          |
| GHZ State                  | [x]      |                                                                                 |
| Graph State                | [-]      | The benchmark as implemented does nothing.                                      |
| Grover                     | [x]      | Touchstone is more configurable. MQT only allows searching for the 1...1 state. |
| QAOA                       | [ ]      | [TODO]                                                                          |
| QFT                        | [x]      | The benchmark here does not make much sense.                                    |
| QFT (entangled)            | [x]      | We take a different approach to QFT benchmarking.                               |
| QNN                        | [ ]      | [TODO]                                                                          |
| Phase Estimation (exact)   | [ ]      | [TODO]                                                                          |
| Phase Estimation (inexact) | [ ]      | [TODO]                                                                          |
| Quark Cardinality          | [ ]      | [TODO]                                                                          |
| Quark Copula               | [ ]      | [TODO]                                                                          |
| Random Walk                | [ ]      | [TODO]                                                                          |
| Random Circuit             | [-]      | Not a meaningful algorithmic benchmark.                                         |
| Shor                       | [ ]      | [TODO]                                                                          |
| VQE Real Amplitude         | [ ]      | [TODO]                                                                          |
| VQE SU(2)                  | [ ]      | [TODO]                                                                          |
| VQE Two Local              | [ ]      | [TODO]                                                                          |
| W State                    | [x]      |                                                                                 |

## NWQBench

Last updated: April 28, 2025

[NWQBench](https://github.com/pnnl/nwqbench) presents a large corpus of quantum benchmark routine generators, written in Python. These benchmarking schemes generated are compatible with the languages PyQuil, Q#, Qiskit, and Cirq.

| Algorithm          | Covered? | Notes                                                                       |
| :----------------- | :------- | :-------------------------------------------------------------------------- |
| Adder              | [x]      | Touchstone is more configurable.                                            |
| Bernstein-Vazirani | [x]      | Touchstone is more configurable.                                            |
| Binary Welded Tree | [ ]      | [TODO]                                                                      |
| Cat State          | [x]      | This is identical to GHZ state preparation.                                 |
| CC                 | [ ]      | [TODO] What is this?                                                        |
| GHZ State          | [x]      | They incorrectly have a Cat state module which yields an identical circuit. |
| Grover             | [x]      | Touchstone is more configurable.                                            |
| HHL                | [ ]      | [TODO]                                                                      |
| Ising              | [ ]      | [TODO]                                                                      |
| Multiplier         | [ ]      | [TODO]                                                                      |
| Square Root        | [ ]      | [TODO]                                                                      |
| SAT                | [ ]      | [TODO]                                                                      |
| W State            | [x]      |                                                                             |

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
