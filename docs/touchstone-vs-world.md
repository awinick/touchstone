# Touchstone vs The World

This page tracks how Touchstone's algorithm and Hamiltonian suite compare against common open-source quantum libraries and industry benchmarking standards.

Use this page to see which structured assets Touchstone provides today, and what areas are still growing.

## QED-C

The [QC-App-Oriented-Benchmarks](https://github.com/SRI-International/QC-App-Oriented-Benchmarks) project, developed under the Quantum Economic Development Consortium (QED-C), defines a set of application-focused quantum algorithms and benchmark tasks.

| Algorithm              | Covered? | Notes                                                                                                                                 |
| :--------------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------ |
| Amplitude Estimation   | [x]      | Touchstone is more configurable.                                                                                                      |
| Bernstein-Vazirani     | [x]      | Touchstone is more configurable.                                                                                                      |
| Deutsch-Jozsa          | [ ]      | [TODO]                                                                                                                                |
| Grover                 | [ ]      | [TODO]                                                                                                                                |
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

[Supermarq](https://github.com/Infleqtion/client-superstaq/) is a suite of application-oriented benchmarks used to measure the performance of quantum computing systems.

| Algorithm                 | Covered? | Notes                                                                                                                                     |
| :------------------------ | :------- | :---------------------------------------------------------------------------------------------------------------------------------------- |
| Bit Code                  | [ ]      | [TODO]                                                                                                                                    |
| GHZ                       | [x]      |                                                                                                                                           |
| Hamiltonian Simulation    | [ ]      | 1D TFIM for Molybdenum diselenide.                                                                                                        |
| Mermin Bell               | [x]      | Touchstone provides circuits for GHZ state preparation. Support for simultaneous Mermin operator measurement and scoring is beyond scope. |
| Phase Code                | [ ]      | [TODO]                                                                                                                                    |
| QAOA Fermionic Swap Proxy | [ ]      | Need to read more. [TODO]                                                                                                                 |
| QAOA Vanilla Proxy        | [ ]      | MaxCut on a Sherrington-Kirkpatrick (SK) model. [TODO]                                                                                    |
| VQE Proxy                 | [ ]      | Need to read more. [TODO]                                                                                                                 |

## Open QBench

[Open QBench](https://quantum.psnc.pl/openqbench/) provides raw QASM for a restricted set of circuits with a fixed width and depth for each benchmark.

| Algorithm   | Covered? | Notes  |
| :---------- | :------- | :----- |
| Grover      | [ ]      | [TODO] |
| QFT         | [ ]      | [TODO] |
| VQE (UCCSD) | [ ]      | [TODO] |
| QAOA (JSSP) | [ ]      | [TODO] |
| QSVM        | [ ]      | [TODO] |

## QPack

[QPack](https://github.com/koenmesman/QPack) aims to set the standard for evaluating quantum-hardware and simulators, using meaningful metrics and practical applications.

| Algorithm          | Covered? | Notes  |
| :----------------- | :------- | :----- |
| Dominating set     | [ ]      | [TODO] |
| Maxcut             | [ ]      | [TODO] |
| Traveling salesman | [ ]      | [TODO] |

## MQT Bench

[MQT Bench](https://github.com/munich-quantum-toolkit/bench) is a quantum circuit benchmark suite with cross-level support, i.e., providing the same benchmark algorithms for different abstraction levels throughout the quantum computing software stack.

Thoughts for future: [NWQBench](https://github.com/pnnl/nwqbench/) -> [QASMBench](https://github.com/pnnl/QASMBench)-> [Benchpress](https://github.com/Qiskit/benchpress/tree/main)

HamLib will have some coverage, [Feynman](https://github.com/meamy/feynman) isn't clear what we would cover.... see Benchpress internals.

[QBraid](https://github.com/qBraid/qbraid-algorithms/)

[QCWare](https://forge.qcware.com)

[BACQ](https://arxiv.org/pdf/2403.12205)

[BenchQC](https://arxiv.org/abs/2504.11204)

[TKET Benchmarks](https://github.com/CQCL/tket_benchmarking)
[AppQSim](https://arxiv.org/abs/2503.04298)
