import pandas as pd
import joblib

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


# ==========================================
# 1. Load feature dataset
# ==========================================

file_path = "data/server_features.csv"

df = pd.read_csv(file_path)


print("\n========== DATA LOADED ==========\n")

print("Rows:", len(df))
print("Columns:", len(df.columns))


# ==========================================
# 2. Select ML features
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


X = df[features].copy()


# ==========================================
# 3. Handle missing/infinite values
# ==========================================

X = X.replace([float("inf"), float("-inf")], 0)

X = X.fillna(0)


# ==========================================
# 4. Scale the data
# ==========================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)


# ==========================================
# 5. Create Isolation Forest
# ==========================================

model = IsolationForest(
    n_estimators=200,
    contamination=0.05,
    random_state=42
)


# ==========================================
# 6. Train model
# ==========================================

model.fit(X_scaled)


print("\nModel training completed!")


# ==========================================
# 7. Predict anomalies
# ==========================================

predictions = model.predict(X_scaled)


# Isolation Forest:
#  1  = Normal
# -1  = Anomaly

df["anomaly_prediction"] = predictions


# ==========================================
# 8. Create anomaly score
# ==========================================

raw_scores = model.decision_function(X_scaled)

df["anomaly_score"] = raw_scores


# ==========================================
# 9. Convert prediction to readable status
# ==========================================

df["status"] = df["anomaly_prediction"].apply(
    lambda x: "ANOMALY" if x == -1 else "NORMAL"
)


# ==========================================
# 10. Count anomalies
# ==========================================

total_anomalies = (
    df["status"] == "ANOMALY"
).sum()


total_normal = (
    df["status"] == "NORMAL"
).sum()


print("\n========== MODEL RESULTS ==========\n")

print("Total records:", len(df))

print("Normal records:", total_normal)

print("Anomalies detected:", total_anomalies)


# ==========================================
# 11. Display anomalies
# ==========================================

anomalies = df[
    df["status"] == "ANOMALY"
]


print("\n========== DETECTED ANOMALIES ==========\n")

print(
    anomalies[
        [
            "timestamp",
            "cpu_usage",
            "ram_usage",
            "active_connections",
            "response_time_ms",
            "anomaly_score",
            "status"
        ]
    ].to_string(index=False)
)


# ==========================================
# 12. Save results
# ==========================================

output_file = "data/anomaly_results.csv"

df.to_csv(
    output_file,
    index=False
)


# ==========================================
# 13. Save ML model
# ==========================================

joblib.dump(
    model,
    "models/isolation_forest.pkl"
)


# Save scaler
joblib.dump(
    scaler,
    "models/scaler.pkl"
)


print("\n========================================")
print("Anomaly detection completed!")
print("========================================")

print("\nResults saved to:")

print(output_file)

print("\nModel saved to:")

print("models/isolation_forest.pkl")

print("\nScaler saved to:")

print("models/scaler.pkl")