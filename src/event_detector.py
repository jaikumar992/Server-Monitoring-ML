import pandas as pd


# Load anomaly results
df = pd.read_csv("data/anomaly_results.csv")


# -----------------------------------------
# Calculate normal baseline
# -----------------------------------------

normal_data = df[df["status"] == "NORMAL"]


normal_cpu = normal_data["cpu_usage"].mean()
normal_ram = normal_data["ram_usage"].mean()
normal_connections = normal_data["active_connections"].mean()
normal_response = normal_data["response_time_ms"].mean()


# -----------------------------------------
# Find anomalies
# -----------------------------------------

anomalies = df[df["status"] == "ANOMALY"].copy()


print("\n========================================")
print("       SERVER EVENT DETECTOR")
print("========================================")


print("\nNormal baseline:")
print(f"CPU: {normal_cpu:.2f}%")
print(f"RAM: {normal_ram:.2f}%")
print(f"Connections: {normal_connections:.0f}")
print(f"Response Time: {normal_response:.2f} ms")


# -----------------------------------------
# Analyze every anomaly
# -----------------------------------------

for index, row in anomalies.iterrows():

    events = []

    cpu = row["cpu_usage"]
    ram = row["ram_usage"]
    connections = row["active_connections"]
    response = row["response_time_ms"]


    # CPU analysis
    if cpu > normal_cpu * 2:
        events.append(
            f"CPU usage unusually high ({cpu:.1f}%)"
        )


    # RAM analysis
    if ram > normal_ram * 1.10:
        events.append(
            f"RAM usage unusually high ({ram:.1f}%)"
        )


    # Connection analysis
    if connections > normal_connections * 2:
        events.append(
            f"Active connections unusually high ({connections:.0f})"
        )


    # Response time analysis
    if response > normal_response * 2:
        events.append(
            f"Response time unusually high ({response:.0f} ms)"
        )


    # -----------------------------------------
    # Determine severity
    # -----------------------------------------

    if len(events) >= 3:
        severity = "HIGH"

    elif len(events) == 2:
        severity = "MEDIUM"

    else:
        severity = "LOW"


    # -----------------------------------------
    # Print event
    # -----------------------------------------

    print("\n")
    print("🚨 SERVER ANOMALY DETECTED")
    print("----------------------------------------")

    print("Time:", row["timestamp"])

    print(f"CPU: {cpu:.1f}%")
    print(f"RAM: {ram:.1f}%")
    print(f"Connections: {connections:.0f}")
    print(f"Response Time: {response:.2f} ms")

    print("\nSeverity:", severity)

    print("\nPossible reasons:")

    if events:

        for event in events:
            print("🔴", event)

    else:

        print(
            "🟡 Unusual combination of server metrics"
        )

    print("----------------------------------------")


print("\n========================================")
print("Event detection completed.")
print("========================================")