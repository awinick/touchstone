# Usage

Touchstone is designed to make benchmarking canonical quantum circuits easy and composable.

### Instantiate and build a circuit

```python
from touchstone.algorithms import BernsteinVazirani

bv = BernsteinVazirani("101")
circuit = bv.build()
circuit.draw()
```