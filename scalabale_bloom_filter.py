# ========================================================================
# Scalable Bloom Filter Implementation
#
# Autor: Tushar
# Date: 2025-12-05
#
# Library Imported : bloom_filter.py
# ========================================================================

from bloom_filter import BloomFilter

class ScalableBloomFilter:
    def __init__(self, initial_fpr = 0.01, initial_n = 1000, tightening_ratio=0.5):
        self.filters = []
        self.tightening_ratio = tightening_ratio
        self.current_fpr = initial_fpr
        self.current_n = initial_n
        self.add_filter()

    def add_filter(self):
        bf = BloomFilter(fpr=self.current_fpr, n=self.current_n)
        self.filters.append(bf)
        # Update for next filter with constant number of elements but tighter FPR
        self.current_fpr *= self.tightening_ratio

    def add(self, items):
        for item in items:
            # Add to the most recent filter
            self.filters[-1].add([item])
            # If the most recent filter is full, add a new filter
            if self._is_full(self.filters[-1]):
                self.add_filter()

    def contains(self, item):
        return any(bf.contains(item) for bf in self.filters)
    
    def _is_full(self, bf):
        ones = bf.bit_array.count(True)
        load_factor = ones / bf.m
        return load_factor > 0.5
    
    def scaled_theoretical_fpr(self):
        total_fpr = 1.0
        for bf in self.filters:
            total_fpr *= (1 - bf.theoretical_fpr())
        return 1 - total_fpr