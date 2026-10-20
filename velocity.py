import pandas as pd
from scipy.stats import median_abs_deviation, norm

def robust_zscore(serise):
  serise = serise.astype(float)
  median = serise.median()
  mad = max(median_abs_deviation(serise, nan_policy="omit"), 1e-6)
  return (serise - median) / mad

    # Compute the Median Absolute Deviation (MAD), a robust measure of spread
    # similar to standard deviation but less sensitive to outliers.
    # Ensure MAD is never too close to zero.
    # max(..., 1e-6) sets a minimum value of 0.000001.
    #
    # Why?
    # - If all values in the series are identical (or nearly identical),
    #   MAD can become 0.
    # - Later calculations may divide by MAD.
    # - Division by 0 would cause errors or extremely unstable values.
    #
    # Using a tiny floor value (1e-6) prevents numerical instability.


def velocity (df, WINDOWS):

  df = df.copy()

  df["short_velocity"] = df["y"].rolling(WINDOWS['short']).mean().diff()
  df["medium_velocity"] = df["y"].rolling(WINDOWS['medium']).mean().diff()
  df["long_velocity"] = df["y"].rolling(WINDOWS['long']).mean().diff()

  df["y_zscore"] = robust_zscore(df["y"])
  df["short_velocity_zscore"] = df["y_zscore"].rolling(WINDOWS['short']).mean().diff()
  df["medium_velocity_zscore"] = df["y_zscore"].rolling(WINDOWS['medium']).mean().diff()
  df["long_velocity_zscore"] = df["y_zscore"].rolling(WINDOWS['long']).mean().diff()

  # df = df.dropna(subset= ['short_velocity', 'medium_velocity', 'long_velocity',
  #      'y_zscore', 'short_velocity_zscore', 'medium_velocity_zscore',
  #      'long_velocity_zscore'])

  return df

# Usage 
# velocity_df = velocity(composite_df, WINDOWS)
# velocity_df.head(10)