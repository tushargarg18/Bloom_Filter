# ========================================================================
# 
# Designing a Bloom Filter for a Target FPR
# Core tasks: 
#   Implement a Bloom filter; 
#   choose m, k for given n and target FPR; 
#   validate measured vs. theoretical FPR.
# Deliverables: Small library, test suite, and report.
# Stretch goal: Scalable/partitioned Bloom filter variant.
# Scope notes: Use m ≈ − n ln(FPR)/(ln 2)2 and k ≈ m/n ln 2 as baselines; 
# test FPR = 1% and 0.1%.
#
# Autor: Tushar
# Date: 2025-11-29
#
# ========================================================================

import math
import mmh3
from bitarray import bitarray

class BloomFilter:
    def __init__(self, fpr, n):
        self.n = n
        self.fpr = fpr
        self.m = int(n * (math.log(fpr) * -1) / (math.log(2) ** 2))
        self.k = int((self.m / n) * math.log(2))
        # Replace list with bitarray for memory efficiency
        self.bit_array = bitarray(self.m)
        self.bit_array.setall(0)
        #self.bit_array = [0] * self.m
        print(f'Initialized BloomFilter with m={self.m}, k={self.k}')

    def _hashes(self, item):
        h1 = mmh3.hash(item, 41, signed = True)
        h2 = mmh3.hash(item, 42, signed = True)
        return [(h1 + i * h2) % self.m for i in range(self.k)]
    
    def add(self, items):
        for i in items:
            for hash_val in self._hashes(i):
                self.bit_array[hash_val] = 1

    def contains(self, item):
        return all(self.bit_array[hash_val] for hash_val in self._hashes(item))
    
    # function to calculate theoretical FPR
    def theoretical_fpr(self):
        return (1 - math.exp(-self.k * self.n / self.m)) ** self.k
    
    # function to calculate measured FPR
    def measured_fpr(self, test_items, actual_items):
        false_positives = sum(1 for item in test_items if self.contains(item) and item not in actual_items)
        return false_positives / len(test_items)
    
    # save the array to a file
    def save_data(self, filename):
        with open(filename, "w") as f:
            for num in self.bit_array:
                f.write(f"{num}\n")

    # Load the array from a file
    def load_data(self, filename):
        with open(filename, "r") as f:
            self.bit_array = [int(line.strip()) for line in f.readlines()]
