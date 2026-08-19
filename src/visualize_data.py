import pandas as pd
import matplotlib.pyplot as plt


# Load data
df = pd.read_csv("data/server_metrics.csv")


# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])


# -------------------------------
# CPU Usage
# -------------------------------

plt.figure(figsize=(12, 5))

plt.plot(
    df["timestamp"],
    df["cpu_usage"]
)

plt.title("CPU Usage Over Time")

plt.xlabel("Time")

plt.ylabel("CPU Usage (%)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()


# -------------------------------
# RAM Usage
# -------------------------------

plt.figure(figsize=(12, 5))

plt.plot(
    df["timestamp"],
    df["ram_usage"]
)

plt.title("RAM Usage Over Time")

plt.xlabel("Time")

plt.ylabel("RAM Usage (%)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()


# -------------------------------
# Response Time
# -------------------------------

plt.figure(figsize=(12, 5))

plt.plot(
    df["timestamp"],
    df["response_time_ms"]
)

plt.title("Response Time Over Time")

plt.xlabel("Time")

plt.ylabel("Response Time (ms)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()