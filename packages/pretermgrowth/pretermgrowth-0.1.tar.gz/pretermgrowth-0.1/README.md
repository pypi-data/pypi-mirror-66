# fenton-growth-calculator
A python package for calculating preterm infant growth statistics.

Currently you can calculate z-scores for infants between ages 22w4d-50w0d.

```python
from pretermgrowth.fenton import Fenton

Fenton.calc_zscore(
    metric="weight", # or "length" or "hc"
    sex="f", # or "m"
    gestational_age_in_days=158, # range = [158-350]
    measure=2400.0 # g for weight, cm for length or hc
)
```

### fenton calculations
Fenton TR and Kim JH, BMC Pediatrics 2013, 13:59 http://www.ncbi.nlm.nih.gov/pubmed/23601190
