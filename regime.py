def classify_regime (row, 
                    spike_threshold = SPIKE_THRESHOLD,
                    building_threshhold = BUILD_THRESHOLD,
                    collapse_threshold = SPIKE_THRESHOLD
                    ):
    sz = row["short_velocity_zscore"]
    lz = row["long_velocity_zscore"]

    if pd.isna(sz):
        return "Insufficient Data"

    crossover = (sz - lz) if pd.notna(lz) else 0

    if sz > spike_threshold and crossover >= 0:
        return "Spike"
    
    elif sz > building_threshhold and crossover >= 0:
        return "Building"
    
    elif sz < -collapse_threshold or ((pd.notna(lz)) and crossover < -1 and lz > 0 ):
        return "Collapsing"

    else :
        return "Quiet"

# Usage     
# velocity_df["regime"] = velocity_df.apply(classify_regime, axis = 1) 
# velocity_df["regime"].value_counts()
# velocity_df.head()