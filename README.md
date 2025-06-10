# qoe-live

This repository contains code from the following paper:
 - Somiya Kapoor, Ethan Witwer, David Hasselquist, Mikael Asplund, and Niklas Carlsson. "Predicting Video QoE from Encrypted Traffic: Leveraging Video Fingerprinting and Providing System-Level Insights". Proceedings of the 2025 IFIP Networking Conference, 2025.

If you use the code in this repository or the linked datasets in your work, please include a reference to the paper.

## Overview

We provide scripts to compute three metrics from a dataset of video QoE log files, such as [LongEnough](https://github.com/trafnex/raising-the-bar):
 - Mean utility (`mean_utility.py`)
 - Rebuffering ratio (`rebuffering_ratio.py`)
 - Switching rate (`switching_rate.py`)

Combined, these three metrics can be used to compute an overall QoE score in the way described in the paper.

Implementations of the traffic analysis attacks adapted for use in the paper, Video-Adapted DF (vDF) and Video-Adapted RF (vRF), can be found [here](https://github.com/trafnex/video-augmentation).

## Setup Tasks

You will need `python3`/`pip` to run the code; they can be downloaded via your distribution's package manager. For example:

```bash
  sudo apt update
  sudo apt install python3 python3-pip
```

## Code Usage

All scripts take two positional arguments: a path to the dataset root (`input_dir`) and a CSV file to save results to (`output_csv`). The script for rebuffering ratio takes a third optional positional argument, the session duration in segments (`duration`, default 60.0). The time spent rebuffering is divided by this value to calculate the rebuffering ratio.

The output is a CSV file with the following columns:
 - Mean utility: ['Path', 'Mean Utility']
 - Rebuffering ratio: ['Path', 'Total Buffering Time (seconds)', 'Rebuffering Ratio']
 - Switching rate: ['Path', 'Quality Changes', 'Switching Rate']

Here, the path corresponds to the file in the dataset which the results were calculated from.

## Datasets

We use an extended version of the _LongEnough_ dataset, which contains traffic traces and QoE metric data for three additional bandwidth scales.

It is available in the same location as the original _LongEnough_ dataset: [https://liuonline-my.sharepoint.com/:f:/g/personal/davha914_student_liu_se/ErK6esYd5IdOiuvfLnXK6NoBEdlj579MlXBvG2wkfQEozg?e=sCHtWp](https://liuonline-my.sharepoint.com/:f:/g/personal/davha914_student_liu_se/ErK6esYd5IdOiuvfLnXK6NoBEdlj579MlXBvG2wkfQEozg?e=sCHtWp)

More details are provided in the dataset README.

## License Info

The code in this repository is available under the terms of the BSD-3-Clause license.
