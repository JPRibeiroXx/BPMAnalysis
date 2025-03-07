import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import (
    find_peaks,
    savgol_filter,
    medfilt
)
from scipy.ndimage import gaussian_filter1d

# ------------------------------------------------------------------------
# 1) Load CSV and rename columns
# ------------------------------------------------------------------------

file_path = "" # Add the path to the CSV file here

try:
    data = pd.read_csv(file_path)
except FileNotFoundError:
    print("Error: CSV file not found. Ensure the correct path is used.")
    exit()

# Rename "Mean" -> "Region" (as when extracted from Fiji the CSV has "Mean" in the column names)
data.rename(
    columns={col: col.replace("Mean", "Region") for col in data.columns if "Mean" in col},
    inplace=True
)

# ------------------------------------------------------------------------
# 2) Define multiple filter functions
# ------------------------------------------------------------------------

def no_filter(values):
    """Return the original data."""
    return values

def moving_average(values, window=5):
    """Apply a rolling average for smoothing."""
    return pd.Series(values).rolling(window=window, center=True).mean().fillna(method='bfill')

def savgol(values, window=11, poly=3):
    """Apply Savitzky-Golay filter for smoothing while preserving peaks."""
    return savgol_filter(values, window_length=window, polyorder=poly)

def gaussian(values, sigma=2):
    """Apply Gaussian smoothing."""
    return gaussian_filter1d(values, sigma=sigma)

def median(values, kernel_size=5):
    """Apply a median filter for outlier removal."""
    return medfilt(values, kernel_size=kernel_size)

# Dictionary mapping filter names to functions
filter_methods = {
    "NoFilter": no_filter,
    "MovingAvg": moving_average,
    "SavGol": savgol,
    "Gaussian": gaussian,
    "Median": median
}

# ------------------------------------------------------------------------
# 3) Main Analysis Parameters
# ------------------------------------------------------------------------

frame_rate = 25  # Frames per second (adjust if needed)
frame_interval = 1 / frame_rate  # Seconds per frame

# Identify ROI columns (now "Region" columns)
roi_columns = [col for col in data.columns if "Region" in col]

# ------------------------------------------------------------------------
# 4) Analyze data with each filter, detect peaks, compute BPM
# ------------------------------------------------------------------------

bpm_results_list = []  # Each entry is (ROI, FilterName, BPM)

for filter_name, filter_func in filter_methods.items():
    plt.figure(figsize=(12, 6))

    # Collect BPMs across all ROIs for this filter (to compute an average for the plot)
    filter_bpm_values = []
    
    for roi in roi_columns:
        # Extract raw intensity
        intensity_values = data[roi].values
        
        # Apply the selected filter
        filtered_values = filter_func(intensity_values)
        
        # Detect peaks
        peaks, _ = find_peaks(
            filtered_values,
            height=np.mean(filtered_values),  # must be above mean
            distance=10                       # min distance in frames between peaks
        )
        
        # Compute BPM
        total_duration_min = len(filtered_values) * frame_interval / 60.0
        bpm = len(peaks) / total_duration_min if total_duration_min > 0 else 0
        
        # Store (ROI, Filter, BPM) for the CSV
        bpm_results_list.append((roi, filter_name, bpm))
        
        # Store BPM to compute the average for plotting
        filter_bpm_values.append(bpm)
        
        # Plot the filtered signal with detected peaks
        plt.plot(filtered_values, label=f"{roi} (BPM: {int(round(bpm))})")
        plt.scatter(peaks, filtered_values[peaks], marker="o", color="red")
    
    # Compute the average BPM across all ROIs for this filter
    avg_bpm = np.mean(filter_bpm_values) if filter_bpm_values else 0
    
    # Finalize plot
    plt.xlabel("Frame Index")
    plt.ylabel("Region Intensity")
    plt.title(f"Beat Detection - {filter_name} (Avg BPM: {int(round(avg_bpm))})")
    plt.legend()

    # Save the figure for this filter
    plot_filename = f"{filter_name}_plot.png"
    plt.savefig(plot_filename, dpi=150)
    plt.close()

# ------------------------------------------------------------------------
# 5) Save Combined BPM Results
# ------------------------------------------------------------------------

bpm_df = pd.DataFrame(bpm_results_list, columns=["ROI", "Filter", "BPM"])

# Name the output CSV using the original file path
output_csv_path = file_path.replace(".csv", "_AllFilters_BPM.csv")
bpm_df.to_csv(output_csv_path, index=False)

print("✅ BPM analysis completed for all filters.")
print("Plots saved as <FilterName>_plot.png in the current directory.")
print(f"BPM results saved to: {output_csv_path}")
