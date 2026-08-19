import pandas as pd
import os


INPUT_FILE = "data/live_results.csv"
OUTPUT_FILE = "data/events.csv"


def create_event(row, previous_row=None):

    events = []

    cpu = row["cpu_usage"]
    ram = row["ram_usage"]
    connections = row["active_connections"]
    response = row["response_time_ms"]

    # CPU
    if cpu >= 80:
        events.append(
            f"High CPU usage: {cpu:.1f}%"
        )

    # RAM
    if ram >= 90:
        events.append(
            f"High RAM usage: {ram:.1f}%"
        )

    # Connections
    if previous_row is not None:

        previous_connections = (
            previous_row["active_connections"]
        )

        if connections > previous_connections * 1.5:
            events.append(
                f"Connection spike: "
                f"{previous_connections:.0f} → "
                f"{connections:.0f}"
            )

    # Response time
    if response >= 1000:
        events.append(
            f"High response time: {response:.0f} ms"
        )

    # If ML says anomaly but no individual
    # metric crossed our explanation thresholds
    if not events:

        events.append(
            "Unusual combination of server metrics"
        )

    return events


def main():

    if not os.path.exists(INPUT_FILE):

        print(
            "live_results.csv not found."
        )

        return

    df = pd.read_csv(INPUT_FILE)

    if df.empty:

        print(
            "No live data available."
        )

        return

    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    df = df.sort_values(
        "timestamp"
    ).reset_index(drop=True)

    events = []

    incident_active = False

    for i, row in df.iterrows():

        previous_row = None

        if i > 0:
            previous_row = df.iloc[i - 1]

        status = row["status"]

        # ==================================
        # NEW ANOMALY
        # ==================================

        if status == "ANOMALY" and not incident_active:

            reasons = create_event(
                row,
                previous_row
            )

            events.append({
                "timestamp": row["timestamp"],
                "event_type": "NEW_ANOMALY",
                "severity": "HIGH",
                "description": " | ".join(reasons)
            })

            incident_active = True

        # ==================================
        # RECOVERY
        # ==================================

        elif status == "NORMAL" and incident_active:

            events.append({
                "timestamp": row["timestamp"],
                "event_type": "RECOVERY",
                "severity": "INFO",
                "description": (
                    "Server metrics returned "
                    "to normal behavior"
                )
            })

            incident_active = False

    # ==================================
    # Save events
    # ==================================

    events_df = pd.DataFrame(events)

    events_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        "\n=================================="
    )

    print(
        "EVENT DETECTION COMPLETED"
    )

    print(
        "=================================="
    )

    print(
        "Events detected:",
        len(events_df)
    )

    print(
        "\nEvents:"
    )

    print(
        events_df.to_string(
            index=False
        )
    )


if __name__ == "__main__":

    main()