# Calculate the mean utility for each QoE log file in a dataset.
# Code from the paper: Somiya Kapoor, Ethan Witwer, David Hasselquist, Mikael
# Asplund, and Niklas Carlsson. "Predicting Video QoE from Encrypted Traffic:
# Leveraging Video Fingerprinting and Providing System-Level Insights".
# Proceedings of the 2025 IFIP Networking Conference, 2025.
# If you use this code in your work, please include a reference to the paper.
# More details are available in README.md

import argparse
import os
import math
import csv

def find_min_max_btr_all(input_dir):
    class_min_max = {}

    for folder in range(100):
        btr_values = []
        for trace in range(10):
            for sample in range(10):
                filename = os.path.join(input_dir, str(folder), f"{folder:04}-{trace:04}-{sample:04}_btr.qoe.log")

                if os.path.exists(filename):
                    with open(filename, 'r') as file:
                        reader = csv.reader(file)
                        next(reader, None)
                        for row in reader:
                            if len(row) >= 2:
                                try:
                                    btr = float(row[1].strip())
                                    btr_values.append(btr)
                                except ValueError:
                                    continue
        if btr_values:
            class_min_max[folder] = (min(btr_values), max(btr_values))
        else:
            class_min_max[folder] = (None, None)
    
    return class_min_max

def extract_btr_segments(file_path):
    btr_data = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if len(row) < 2:
                    return None
                try:
                    btr_value = float(row[1])
                    btr_data.append(btr_value)
                except ValueError:
                    continue
    return btr_data

def calculate_mean_utility(btr_data, min_btr, max_btr, total_segments = 30):
    sum_utility = 0
    for btr in btr_data:
        if min_btr and max_btr and btr > 0:
            sum_utility += math.log(btr / min_btr) / math.log(max_btr / min_btr)
    return round(sum_utility / total_segments, 4) if total_segments > 0 else None

def process_directory(input_dir, output_csv):
    results = []
    class_min_max = find_min_max_btr_all(input_dir)

    for folder in range(100):
        min_btr, max_btr = class_min_max.get(folder, (None, None))
        if min_btr is None or max_btr is None:
            continue
        for trace in range(10):
            for sample in range(10):
                filename = os.path.join(input_dir, str(folder), f"{folder:04}-{trace:04}-{sample:04}_btr.qoe.log")

                if os.path.exists(filename):
                    btr_data = extract_btr_segments(filename)
                    if btr_data:
                        mean_utility = calculate_mean_utility(btr_data, min_btr, max_btr)
                        results.append({'file_path': filename, 'mean_utility': mean_utility})

    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['Path', 'Mean Utility']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", help = "dataset path")
    parser.add_argument("output_csv", help = "output CSV file path, mean utility")
    args = parser.parse_args()

    process_directory(args.input_dir, args.output_csv)
