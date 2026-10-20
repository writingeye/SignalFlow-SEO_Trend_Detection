#config
KEYWORD = "trump"
WEIGHTS = { "search":0.5, "youtube":0.2, "news":0.3 }
WINDOWS = { "short":15, "medium":30, "long":60 }
FORECAST_DAYS = 90
SPIKE_THRESHOLD_LOW = 1.5
SPIKE_THRESHOLD_HIGH = 2.5
STD_CUTOFF = 10
DATA_DIR = "/home/szasz/Documents/CS/code/signal_flow/combined_trends_{KEYWORD}"