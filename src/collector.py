import psutil
import time
import csv
import os
import urllib.request
from datetime import datetime


# CSV file location
file_path = "data/server_metrics.csv"

# Website/server to monitor
target_url = "https://www.google.com"


# Create data folder
os.makedirs("data", exist_ok=True)


# Create CSV file with headers
if not os.path.exists(file_path):

    with open(file_path, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "timestamp",
            "cpu_usage",
            "ram_usage",
            "disk_usage",
            "bytes_sent",
            "bytes_received",
            "packets_sent",
            "packets_received",
            "active_connections",
            "response_time_ms"
        ])


print("====================================")
print(" SERVER MONITORING STARTED")
print("====================================")
print("Monitoring:", target_url)
print("Data file:", file_path)
print("Press CTRL + C to stop.")
print()


while True:

    # -----------------------------
    # CPU
    # -----------------------------

    cpu = psutil.cpu_percent(interval=1)


    # -----------------------------
    # RAM
    # -----------------------------

    ram = psutil.virtual_memory().percent


    # -----------------------------
    # Disk
    # -----------------------------

    disk = psutil.disk_usage("C:\\").percent


    # -----------------------------
    # Network
    # -----------------------------

    network = psutil.net_io_counters()

    bytes_sent = network.bytes_sent
    bytes_received = network.bytes_recv

    packets_sent = network.packets_sent
    packets_received = network.packets_recv


    # -----------------------------
    # Active Connections
    # -----------------------------

    try:

        connections = psutil.net_connections(kind="inet")

        active_connections = len(connections)

    except (psutil.AccessDenied, PermissionError):

        active_connections = -1


    # -----------------------------
    # Response Time
    # -----------------------------

    start_time = time.perf_counter()

    try:

        urllib.request.urlopen(
            target_url,
            timeout=5
        )

        end_time = time.perf_counter()

        response_time_ms = round(
            (end_time - start_time) * 1000,
            2
        )

    except Exception:

        response_time_ms = -1


    # -----------------------------
    # Timestamp
    # -----------------------------

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    # -----------------------------
    # Save data
    # -----------------------------

    with open(file_path, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            timestamp,
            cpu,
            ram,
            disk,
            bytes_sent,
            bytes_received,
            packets_sent,
            packets_received,
            active_connections,
            response_time_ms
        ])


    # -----------------------------
    # Display
    # -----------------------------

    print(
        f"{timestamp} | "
        f"CPU: {cpu}% | "
        f"RAM: {ram}% | "
        f"Disk: {disk}% | "
        f"Sent: {bytes_sent} | "
        f"Received: {bytes_received} | "
        f"Connections: {active_connections} | "
        f"Response: {response_time_ms} ms"
    )


    # Wait before next reading

    time.sleep(5)