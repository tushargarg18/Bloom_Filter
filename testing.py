# ========================================================================
# Testing script for Bloom Filter and Scalable Bloom Filter
#
# Autor: Tushar
# Date: 2025-12-05
#
# Library Imported : bloom_filter.py, scalable_bloom_filter.py
# ========================================================================

import matplotlib.pyplot as plt
import pandas as pd
from bloom_filter import BloomFilter
from scalabale_bloom_filter import ScalableBloomFilter
import os
import sys

# -----------------------------
# Load datasets
# -----------------------------
# Check if results file exists
input = input("Do you want to re-run the tests and overwrite existing results? (y/n): ")
if input.lower() != 'y' and os.path.exists('bloom_filter_test_results.csv'):
    print("Results file already exists. Exiting without re-running tests.")
    df_results = pd.read_csv('bloom_filter_test_results.csv')
else:
    results = []
    scalable_bf_results = []
    print("Re-running tests and overwriting existing results if any.")
    # Elements to test for false positives (not in the datasets)
    test_set1 = [f"test_{i}" for i in range(50000)]
    test_set2 = [f"test_{i}" for i in range(700)]
    
    # Load first dataset - with ~14M titles
    titles_data_path = r"datasets\wikipedia_titles\titles.txt"
    with open(titles_data_path, 'r') as file:
        titles = [line.strip() for line in file.readlines()]
    titles = titles[:100000]  # Limit to first 100,000 titles for testing
    # Load second dataset - IMDB top 1000 movies
    movies_data_path = r"datasets\imdb_movie_dataset\imdb_top_1000.csv"
    movies_df = pd.read_csv(movies_data_path)
    movie_titles = movies_df['Series_Title'].tolist()

    print(f"Loaded {len(titles)} titles from {titles_data_path}")
    print(titles[-5:])  # Print first 5 titles as a sample
    print(f"Loaded {len(movie_titles)} movie titles from {movies_data_path}")
    print(movie_titles[:5])  # Print first 5 movie titles as a sample

    datasets = [
        ("Dataset 1", titles, test_set1),
        ("Dataset 2", movie_titles, test_set2)
    ]

    # -----------------------------
    # Test Bloom Filter
    # -----------------------------
    size = [0.25, 0.5, 0.75, 1, 1.25, 1.5]  # Size factors to test
    for name, dataset, test_set in datasets:
        # Testing the bloom filter initiailization with 6 different number of elements
        # 1. Actual number of elements
        # 2. 1.25 times number of elements
        # 3. 1.5 times number of elements
        # 4. 0.5 times number of elements
        # 5. 0.75 times number of elements
        # 6. 0.25 times number of elements
        for s in size:
            bf = BloomFilter(fpr=0.1, n=int(len(dataset)*s))
            s_bf = ScalableBloomFilter(initial_fpr=0.1, initial_n=int(len(dataset)*s))
            bf.add(dataset)
            s_bf.add(dataset)
            
            # Check for false positives
            false_positives = sum(1 for item in test_set if bf.contains(item))
            scalable_bf_false_positives = sum(1 for item in test_set if s_bf.contains(item))
            actual_fpr = false_positives / len(test_set)
            scalable_bf_actual_fpr = scalable_bf_false_positives / len(test_set)
            theoretical_fpr = bf.theoretical_fpr()
            scalable_bf_theoretical_fpr = s_bf.scaled_theoretical_fpr()

            # Memory usage
            theoretical_bits = bf.m  # Number of bits in the bit array
            theoretical_bytes = theoretical_bits / 8
            theoretical_kb = theoretical_bytes / 1024

            # Actual memory
            actual_bytes = sys.getsizeof(bf) + sys.getsizeof(bf.bit_array)
            actual_kb = actual_bytes / 1024

            # False Negative test
            false_negatives = sum(1 for item in dataset if not bf.contains(item))
            assert false_negatives == 0, f"False negatives detected in {name} with size factor {s}"

            results.append({
                "Dataset": name,
                "Size Factor": s,
                "Inserted Items": len(dataset),
                "Test Items": len(test_set),
                "Actual FPR": actual_fpr,
                "Theoretical FPR": theoretical_fpr,
                "Actual Memory (KB)": actual_kb,
                "Theoretical Memory (KB)": theoretical_kb,
                "false negatives": false_negatives,
                "Scalable BF Actual FPR": scalable_bf_actual_fpr,
                "Scalable BF Theoretical FPR": scalable_bf_theoretical_fpr
            })

    df_results = pd.DataFrame(results)
    print(df_results)
    df_results.to_csv("bloom_filter_test_results.csv", index=False)

# -----------------------------
# Visualize results
# -----------------------------
# Bar plot: Theoretical vs Actual FPR
for dataset_name in df_results["Dataset"].unique():
    df_subset = df_results[df_results["Dataset"] == dataset_name]
    x = df_subset["Size Factor"]
    y_theoretical = df_subset["Theoretical FPR"]
    y_actual = df_subset["Actual FPR"]

    x_indices = range(len(x))
    width = 0.35

    plt.figure(figsize=(10,6))
    plt.bar([i - width/2 for i in x_indices], y_theoretical, width=width, label='Theoretical FPR')
    plt.bar([i + width/2 for i in x_indices], y_actual, width=width, label='Actual FPR')
    plt.xticks(ticks=x_indices, labels=x)
    plt.xlabel("Size Factor")
    plt.ylabel("False Positive Rate")
    plt.title(f"Bloom Filter FPR Comparison for {dataset_name}")
    plt.legend()
    plt.show()

    # Bar plot: Theoretical vs Actual Memory Usage
    y_theoretical_mem = df_subset["Theoretical Memory (KB)"]
    y_actual_mem = df_subset["Actual Memory (KB)"]
    plt.figure(figsize=(10,6))
    plt.bar([i - width/2 for i in x_indices], y_theoretical_mem, width=width, label='Theoretical Memory (KB)')
    plt.bar([i + width/2 for i in x_indices], y_actual_mem, width=width, label='Actual Memory (KB)')
    plt.xticks(ticks=x_indices, labels=x)
    plt.xlabel("Size Factor")
    plt.ylabel("Memory Usage (KB)")
    plt.title(f"Bloom Filter Memory Usage Comparison for {dataset_name}")
    plt.legend()
    plt.show()

    # Bar plot: Scalable Bloom Filter Theoretical vs Actual FPR
    y_scalable_theoretical = df_subset["Scalable BF Theoretical FPR"]
    y_scalable_actual = df_subset["Scalable BF Actual FPR"]
    plt.figure(figsize=(10,6))
    plt.bar([i - width/2 for i in x_indices], y_scalable_theoretical, width=width, label='Scalable BF Theoretical FPR')
    plt.bar([i + width/2 for i in x_indices], y_scalable_actual, width=width, label='Scalable BF Actual FPR')
    plt.xticks(ticks=x_indices, labels=x)
    plt.xlabel("Size Factor")
    plt.ylabel("False Positive Rate")
    plt.title(f"Scalable Bloom Filter FPR Comparison for {dataset_name}")
    plt.legend()
    plt.show()