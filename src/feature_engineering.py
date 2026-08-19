import pandas as pd
import numpy as np


# ==========================================
# 1. Load dataset
# ==========================================

input_file = "data/server_metrics.csv"

df = pd.read_csv(input_file)


# ==========================================
# 2. Convert timestamp
# ==========================================

df["timestamp"] = pd.to_datetime(df["timestamp"])


# Sort data by time
df = df.sort_values("timestamp").reset_index(drop=True)


# ==========================================
# 3. Calculate time difference
# ==========================================

df["time_diff_seconds"] = (
    df["timestamp"].diff().dt.total_seconds()
)


# First row has no previous timestamp
df["time_diff_seconds"] = (
    df["time_diff_seconds"]
    .fillna(1)
)


# Prevent division by zero
df["time_diff_seconds"] = (
    df["time_diff_seconds"].replace(0, 1)
)


# ==========================================
# 4. Calculate network differences
# ==========================================

df["bytes_sent_diff"] = (
    df["bytes_sent"].diff().fillna(0)
)

df["bytes_received_diff"] = (
    df["bytes_received"].diff().fillna(0)
)

df["packets_sent_diff"] = (
    df["packets_sent"].diff().fillna(0)
)

df["packets_received_diff"] = (
    df["packets_received"].diff().fillna(0)
)


# ==========================================
# 5. Calculate network rates
# ==========================================

df["bytes_sent_per_second"] = (
    df["bytes_sent_diff"]
    / df["time_diff_seconds"]
)

df["bytes_received_per_second"] = (
    df["bytes_received_diff"]
    / df["time_diff_seconds"]
)

df["packets_sent_per_second"] = (
    df["packets_sent_diff"]
    / df["time_diff_seconds"]
)

df["packets_received_per_second"] = (
    df["packets_received_diff"]
    / df["time_diff_seconds"]
)


# ==========================================
# 6. Remove negative rates
# ==========================================

rate_columns = [
    "bytes_sent_per_second",
    "bytes_received_per_second",
    "packets_sent_per_second",
    "packets_received_per_second"
]

for column in rate_columns:

    df[column] = df[column].clip(lower=0)


# ==========================================
# 7. Create useful ratios
# ==========================================

df["network_bytes_per_second"] = (
    df["bytes_sent_per_second"]
    + df["bytes_received_per_second"]
)


df["network_packets_per_second"] = (
    df["packets_sent_per_second"]
    + df["packets_received_per_second"]
)


# ==========================================
# 8. Create high-resource indicators
# ==========================================

df["high_cpu"] = (
    df["cpu_usage"] > 80
).astype(int)


df["high_ram"] = (
    df["ram_usage"] > 90
).astype(int)


df["high_response_time"] = (
    df["response_time_ms"] > 1000
).astype(int)


# ==========================================
# 9. Select ML features
# ==========================================

features = [
    "cpu_usage",
    "ram_usage",
    "disk_usage",
    "bytes_sent_per_second",
    "bytes_received_per_second",
    "packets_sent_per_second",
    "packets_received_per_second",
    "active_connections",
    "response_time_ms"
]


# ==========================================
# 10. Check feature data
# ==========================================

print("\n========== FEATURE DATA ==========\n")

print(df[features].head())


print("\n========== FEATURE STATISTICS ==========\n")

print(df[features].describe())


# ==========================================
# 11. Save processed dataset
# ==========================================

output_file = "data/server_features.csv"

df.to_csv(output_file, index=False)


print("\n========================================")
print("Feature engineering completed!")
print("========================================")

print("\nOriginal rows:", len(df))

print("Features created:", len(features))

print("\nSaved to:")

print(output_file)