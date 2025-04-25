# Touchstone

A modern library for benchmarking canonical quantum circuits.

## Example usage

```python
from touchstone.algorithms import BernsteinVazirani

bv = BernsteinVazirani("101")
circuit = bv.build()
```