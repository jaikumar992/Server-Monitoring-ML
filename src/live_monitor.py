import psutil
import time
import joblib
import pandas as pd
import urllib.request
from datetime import datetime


# ==========================================
# Load trained ML model
# ==========================================

model = joblib.load(
    "models/isolation_forest.pkl"
)

scaler = joblib.load(
    "models/scaler.pkl"
)


# ==========================================
# Configuration
# ==========================================

TARGET_URL = "https://www.google.com"

OUTPUT_FILE = "data/live_results.csv"


# ==========================================
# ML features
# ==========================================

FEATURES = [
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
# Previous network counters
# ==========================================

previous_network = psutil.net_io_counters()

previous_time = time.time()


# ==========================================
# Create output CSV
# ==========================================

columns = [
    "timestamp",
    "cpu_usage",
    "ram_usage",
    "disk_usage",
    "bytes_sent_per_second",
    "bytes_received_per_second",
    "packets_sent_per_second",
    "packets_received_per_second",
    "active_connections",
    "response_time_ms",
    "anomaly_score",
    "status"
]


try:

    pd.read_csv(OUTPUT_FILE)

except FileNotFoundError:

    pd.DataFrame(
        columns=columns
    ).to_csv(
        OUTPUT_FILE,
        index=False
    )


print("======================================")
print("     LIVE SERVER MONITORING")
print("======================================")
print()
print("Press CTRL + C to stop.")
print()


# ==========================================
# Monitoring loop
# ==========================================

while True:

    # --------------------------------------
    # Current time
    # --------------------------------------

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    # --------------------------------------
    # CPU
    # --------------------------------------

    cpu = psutil.cpu_percent(
        interval=1
    )


    # --------------------------------------
    # RAM
    # --------------------------------------

    ram = psutil.virtual_memory().percent


    # --------------------------------------
    # Disk
    # --------------------------------------

    disk = psutil.disk_usage(
        "C:\\"
    ).percent


    # --------------------------------------
    # Network
    # --------------------------------------

    current_network = psutil.net_io_counters()

    current_time = time.time()


    time_difference = (
        current_time - previous_time
    )


    if time_difference <= 0:

        time_difference = 1


    bytes_sent_per_second = (
        current_network.bytes_sent
        - previous_network.bytes_sent
    ) / time_difference


    bytes_received_per_second = (
        current_network.bytes_recv
        - previous_network.bytes_recv
    ) / time_difference


    packets_sent_per_second = (
        current_network.packets_sent
        - previous_network.packets_sent
    ) / time_difference


    packets_received_per_second = (
        current_network.packets_recv
        - previous_network.packets_recv
    ) / time_difference


    # --------------------------------------
    # Active connections
    # --------------------------------------

    try:

        active_connections = len(
            psutil.net_connections(
                kind="inet"
            )
        )

    except Exception:

        active_connections = 0


    # --------------------------------------
    # Response time
    # --------------------------------------

    start = time.perf_counter()


    try:

        urllib.request.urlopen(
            TARGET_URL,
            timeout=5
        )

        response_time = (
            time.perf_counter() - start
        ) * 1000

        response_time = round(
            response_time,
            2
        )

    except Exception:

        response_time = 5000


    # --------------------------------------
    # Create feature dataframe
    # --------------------------------------

    data = {

        "cpu_usage": cpu,

        "ram_usage": ram,

        "disk_usage": disk,

        "bytes_sent_per_second":
            max(bytes_sent_per_second, 0),

        "bytes_received_per_second":
            max(bytes_received_per_second, 0),

        "packets_sent_per_second":
            max(packets_sent_per_second, 0),

        "packets_received_per_second":
            max(packets_received_per_second, 0),

        "active_connections":
            active_connections,

        "response_time_ms":
            response_time
    }


    X = pd.DataFrame(
        [data]
    )[FEATURES]


    # --------------------------------------
    # Scale
    # --------------------------------------

    X_scaled = scaler.transform(X)


    # --------------------------------------
    # ML prediction
    # --------------------------------------

    prediction = model.predict(
        X_scaled
    )[0]


    anomaly_score = model.decision_function(
        X_scaled
    )[0]


    if prediction == -1:

        status = "ANOMALY"

    else:

        status = "NORMAL"


    # --------------------------------------
    # Save result
    # --------------------------------------

    result = {

        "timestamp": timestamp,

        **data,

        "anomaly_score":
            anomaly_score,

        "status":
            status
    }


    pd.DataFrame(
        [result]
    ).to_csv(
        OUTPUT_FILE,
        mode="a",
        header=False,
        index=False
    )


    # --------------------------------------
    # Terminal output
    # --------------------------------------

    if status == "ANOMALY":

        print()
        print("🚨🚨🚨 ANOMALY DETECTED 🚨🚨🚨")
        print(
            f"Time: {timestamp}"
        )
        print(
            f"CPU: {cpu:.1f}%"
        )
        print(
            f"RAM: {ram:.1f}%"
        )
        print(
            f"Connections: {active_connections}"
        )
        print(
            f"Response: {response_time:.0f} ms"
        )
        print(
            f"Anomaly Score: {anomaly_score:.4f}"
        )
        print()


    else:

        print(
            f"{timestamp} | "
            f"CPU: {cpu:.1f}% | "
            f"RAM: {ram:.1f}% | "
            f"Response: {response_time:.0f}ms | "
            f"Status: 🟢 NORMAL"
        )


    # --------------------------------------
    # Update previous network values
    # --------------------------------------

    previous_network = current_network

    previous_time = current_time


    # --------------------------------------
    # Wait
    # --------------------------------------

    time.sleep(5)