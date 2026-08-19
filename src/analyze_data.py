import pandas as pd


# Load server data
file_path = "data/server_metrics.csv"

df = pd.read_csv(file_path)


# --------------------------------
# 1. Dataset information
# --------------------------------

print("\n========== DATASET INFO ==========\n")

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\nColumns:")
print(df.columns.tolist())


# --------------------------------
# 2. First 5 records
# --------------------------------

print("\n========== FIRST 5 RECORDS ==========\n")

print(df.head())


# --------------------------------
# 3. Data types
# --------------------------------

print("\n========== DATA TYPES ==========\n")

print(df.dtypes)


# --------------------------------
# 4. Missing values
# --------------------------------

print("\n========== MISSING VALUES ==========\n")

print(df.isnull().sum())


# --------------------------------
# 5. Duplicate records
# --------------------------------

print("\n========== DUPLICATES ==========\n")

print("Duplicate rows:", df.duplicated().sum())


# --------------------------------
# 6. Statistical summary
# --------------------------------

print("\n========== STATISTICS ==========\n")

print(df.describe())


# --------------------------------
# 7. Average server performance
# --------------------------------

print("\n========== AVERAGE VALUES ==========\n")

print("Average CPU:",
      round(df["cpu_usage"].mean(), 2), "%")

print("Average RAM:",
      round(df["ram_usage"].mean(), 2), "%")

print("Average Disk:",
      round(df["disk_usage"].mean(), 2), "%")

print("Average Response Time:",
      round(df["response_time_ms"].mean(), 2), "ms")


# --------------------------------
# 8. Maximum values
# --------------------------------

print("\n========== MAXIMUM VALUES ==========\n")

print("Maximum CPU:",
      df["cpu_usage"].max(), "%")

print("Maximum RAM:",
      df["ram_usage"].max(), "%")

print("Maximum Disk:",
      df["disk_usage"].max(), "%")

print("Maximum Response Time:",
      df["response_time_ms"].max(), "ms")


# --------------------------------
# 9. Minimum values
# --------------------------------

print("\n========== MINIMUM VALUES ==========\n")

print("Minimum CPU:",
      df["cpu_usage"].min(), "%")

print("Minimum RAM:",
      df["ram_usage"].min(), "%")

print("Minimum Disk:",
      df["disk_usage"].min(), "%")

print("Minimum Response Time:",
      df["response_time_ms"].min(), "ms")