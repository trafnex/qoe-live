# Calculate the switching rate for each QoE log file in a dataset.
# Code from the paper: Somiya Kapoor, Ethan Witwer, David Hasselquist, Mikael
# Asplund, and Niklas Carlsson. "Predicting Video QoE from Encrypted Traffic:
# Leveraging Video Fingerprinting and Providing System-Level Insights".
# Proceedings of the 2025 IFIP Networking Conference, 2025.
# If you use this code in your work, please include a reference to the paper.
# More details are available in README.md

import argparse
import os
import csv

def compute_switching_rate(input_directory, output_csv):
    results = []

    for folder in range(100):
        print(f"Processing folder: {folder}")
        for trace in range(10):
            for sample in range(10):
                filename = os.path.join(input_directory, f"{folder}/{folder:04}-{trace:04}-{sample:04}.qoe.log")

                if not os.path.exists(filename):
                    continue

                try:
                    with open(filename, "r") as file:
                        lines = file.readlines()
                except FileNotFoundError:
                    continue

                if not lines:
                    continue

                # Get endTime from the last valid line
                endTime = None
                for line in reversed(lines):
                    parts = line.strip().split(",")
                    if len(parts) < 2:
                        continue
                    try:
                        endTime = float(parts[0])
                        break
                    except ValueError:
                        continue

                if endTime is None:
                    continue

                # Count quality change requests and related events in last 60 seconds
                request_timestamps = []
                quality_change_requests = 0

                for line in lines:
                    parts = line.strip().split(",")
                    if len(parts) < 2:
                        continue

                    try:
                        timestamp = float(parts[0])
                    except ValueError:
                        continue

                    if endTime - timestamp > 60000:
                        continue

                    event = parts[1]

                    if event == "qualityChangeRequested":
                        request_timestamps.append(timestamp)
                    elif event == "qualityChangeRendered":
                        request_timestamps = [t for t in request_timestamps if endTime - t <= 60000]
                        if request_timestamps:
                            quality_change_requests += 1
                            request_timestamps.pop(0)

                # Calculate switching rate
                switching_rate = round(quality_change_requests / 29, 4)  # 30 segments - 1

                results.append({
                    "filename": filename,
                    "quality_changes": quality_change_requests,
                    "switching_rate": switching_rate
                })

    # Write results to CSV
    with open(output_csv, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Path', 'Quality Changes', 'Switching Rate'])
        writer.writeheader()
        for row in results:
            writer.writerow(row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", help = "dataset path")
    parser.add_argument("output_csv", help = "output CSV file path, switching rate")
    args = parser.parse_args()

    compute_switching_rate(args.input_dir, args.output_csv)
