# Bloom Filter Library and Scalable Variant

A Python implementation of **Bloom Filters** and **Scalable Bloom Filters** for probabilistic set membership testing. This library supports insertion, querying, theoretical vs. measured false positive rate (FPR) calculations, and memory-efficient storage using `bitarray`.

---

## Features

- Standard **Bloom Filter**:
  - Add items and check membership.
  - Calculate **theoretical FPR** and **measured FPR**.
  - Memory-efficient storage using `bitarray`.
  - Save and load bit arrays to/from a file.

- **Scalable Bloom Filter (Stretch Goal)**:
  - Dynamically grows by adding new filters with progressively tighter FPR.
  - Maintains predictable FPR for growing datasets.
  - Prevents excessive false positives without reallocating the entire filter.

- Tested on **real-world datasets**:
  - Wikipedia article titles
  - IMDb Top 1000 Movies & TV Shows

---

## Install the dependencies
pip install -r requirements.txt

## Usage

### Standard Bloom Filter
- Initialize with a target false positive rate (`fpr`) and expected number of items (`n`).
- Add items using `add()`.
- Check membership using `contains()`.
- Compute theoretical or measured FPR.
- Save and load bit arrays from a file.

### Scalable Bloom Filter
- Initialize with an initial FPR, initial number of items, and tightening ratio.
- Add items dynamically; the filter grows automatically as needed.
- Check membership using `contains()`.
- Retrieve scaled theoretical FPR across all internal filters.

### Example
```python
from bloom_filter import BloomFilter
from scalable_bloom_filter import ScalableBloomFilter

# Standard Bloom Filter
bf = BloomFilter(fpr=0.01, n=1000)
bf.add(['apple', 'banana'])
print(bf.contains('apple'))  # True

# Scalable Bloom Filter
sbf = ScalableBloomFilter(initial_fpr=0.01, initial_n=1000, tightening_ratio=0.5)
sbf.add(['apple', 'banana'])
print(sbf.contains('grape'))  # False

