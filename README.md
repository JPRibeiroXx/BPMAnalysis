# BPM Analysis and Filtering Script

This repository contains a Python script for analyzing peaks in cardiac beating data using filtering techniques. The script detects peaks in a time-series signal—representing cardiomyocyte contractions—by leveraging functions from the `scipy` library. It then applies noise reduction using the Savitzky–Golay filter to smooth the data, enhancing the accuracy of peak detection.

## Features

- **Peak Detection:**  
  Identifies peaks in the signal corresponding to individual cardiac beats.
  
- **Noise Reduction:**  
  Applies the Savitzky–Golay filter (and other techniques) to smooth the raw data and minimize noise.

- **Visualization:**  
  Generates plots comparing raw and filtered signals to provide visual confirmation of peak analysis.

## Dependencies

This script requires the following Python packages:
- `numpy`
- `scipy`
- `matplotlib`

Install the dependencies with:
```bash
pip install numpy scipy matplotlib
```
## Usage

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/BPM_Analysis_Filtering.git
   cd BPM_Analysis_Filtering
   ```
2. **Run the Script:**
   ```bash
   python BPM_Analysis_Filtering.py
   ```
   
The script will load the input data, perform peak detection and filtering, and then display plots for analysis.

## Code Overview

- **Data Input:**  
  Loads a time-series signal that reflects the beating activity of cardiomyocytes.

- **Peak Detection:**  
  Utilizes `scipy.signal.find_peaks` to locate peaks in the data, which represent individual beats.

- **Filtering:**  
  Applies the Savitzky–Golay filter (via `scipy.signal.savgol_filter`) to reduce noise and smooth the signal, thereby improving the robustness of peak detection.

- **Plotting:**  
  Uses `matplotlib` to plot both raw and filtered data, along with the detected peaks, for visual inspection.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
