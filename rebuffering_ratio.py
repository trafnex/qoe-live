# Calculate the rebuffering ratio for each QoE log file in a dataset.
# Code from the paper: Somiya Kapoor, Ethan Witwer, David Hasselquist, Mikael
# Asplund, and Niklas Carlsson. "Predicting Video QoE from Encrypted Traffic:
# Leveraging Video Fingerprinting and Providing System-Level Insights".
# Proceedings of the 2025 IFIP Networking Conference, 2025.
# If you use this code in your work, please include a reference to the paper.
# More details are available in README.md

import argparse
import csv
import os

def calculate_buffer_time(log_file_path, session_duration):
    total_buffer_time = 0
    buffer_stalled_time = None

    try:
        with open(log_file_path, 'r') as log_file:
            reader = csv.reader(log_file)

            # Skip headers if they exist
            headers = next(reader, None)
            if headers and len(headers) < 2:
                print(f"Skipping file {log_file_path} due to malformed header.")
                return None

            for row in reader:
                if len(row) < 2:
                    print(f"Skipping malformed row: {row}")
                    continue

                # Assuming the time is in the first column and the event is in the second column
                timestamp = float(row[0])
                event = row[1]

                if event == 'bufferStalled':
                    buffer_stalled_time = timestamp
                elif event == 'bufferLoaded' and buffer_stalled_time is not None:
                    # Calculate the time difference
                    buffer_time = timestamp - buffer_stalled_time
                    total_buffer_time += buffer_time
                    buffer_stalled_time = None



        # Calculate the rebuffering ratio
        rebuffering_ratio = total_buffer_time / session_duration

        return total_buffer_time, round(rebuffering_ratio, 3)
    except FileNotFoundError:
        print(f"Error: The file at {log_file_path} was not found.")
        return None, None
    except Exception as e:
        print(f"An error occurred while processing {log_file_path}: {e}")
        return None, None

def process_directory(directory_path, output_csv, session_duration):
    results = []

    # Walk through the directory to find all qoe.log files
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.qoe.log'):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                buffer_time, rebuffering_ratio = calculate_buffer_time(file_path, session_duration)
                if buffer_time is not None:
                    results.append([file, buffer_time, rebuffering_ratio])

    # Write results to a CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Path', 'Total Buffering Time (seconds)', 'Rebuffering Ratio'])
        writer.writerows(results)

    print(f"Results saved to {output_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", help = "dataset path")
    parser.add_argument("output_csv", help = "output CSV file path, rebuffering ratio")
    parser.add_argument("duration", help = "session duration in seconds", type = float, default = 60.0)
    args = parser.parse_args()
    
    process_directory(args.input_dir, args.output, args.duration)
