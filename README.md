# Touchstone

**touch·stone** 
*/ˈtəCHˌstōn/* • *noun*
> **1.** a standard or criterion by which something is judged or recognized.
>
> **2.** a hard stone used to test the purity of gold or silver by the streak left on its surface.
>
>Touchstone isn’t a transpiler. It’s a measure.  
>We give you the stone. You decide what to do with it.

**Touchstone** is a modern library for generating benchmark quantum circuits focusing on clarity, composability, and usability.

---

### Why Touchstone?

Most quantum benchmarking tools today are either overly academic or painfully inflexible. Touchstone is a fresh take on what circuit benchmarking should be:

- Built for experimentation, not just file dumping
- Minimal or highly configurable — and everything in between
- Modular circuit construction with intuitive tags and filters
- Ready for real benchmarking workflows, from transpiler evaluation to device performance tracking

### Example Usage

```python
import touchstone as ts

algorithms = ts.filter_algorithms(ts.tag.SIMULABLE, ts.tag.DETERMINISTIC)

algorithm_instances = ts.instantiate_by(
    algorithms,
    min_num_qubits = 4,
    max_num_qubits = 50,
)

# Option 1: Create a dictionary of Qiskit circuits
circuits = ts.build(algorithm_instances)

# Option 2: Save the circuits as QASM
ts.build(algorithm_instances, type=ts.QASM, dir="circuits")
```
