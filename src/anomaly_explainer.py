import pandas as pd
import os

INPUT_FILE = "data/live_results.csv"
OUTPUT_FILE = "data/events.csv"


def explain_anomaly(row, previous_row=None):

    reasons = []

    cpu = row["cpu_usage"]
    ram = row["ram_usage"]
    connections = row["active_connections"]
    response = row["response_time_ms"]

    # CPU
    if cpu >= 80:
        reasons.append(
            f"High CPU usage ({cpu:.1f}%)"
        )

    # RAM
    if ram >= 90:
        reasons.append(
            f"High RAM usage ({ram:.1f}%)"
        )

    # Response time
    if response >= 1000:
        reasons.append(
            f"Slow response time ({response:.0f} ms)"
        )

    # Connection spike
    if previous_row is not None:

        previous_connections = previous_row[
            "active_connections"
        ]

        if connections > previous_connections * 1.5:

            reasons.append(
                f"Connection spike "
                f"({previous_connections:.0f} → "
                f"{connections:.0f})"
            )

    if not reasons:

        reasons.append(
            "Unusual combination of server metrics"
        )

    return reasons


def calculate_severity(reasons):

    number_of_reasons = len(reasons)

    if number_of_reasons >= 3:
        return "CRITICAL"

    elif number_of_reasons == 2:
        return "HIGH"

    elif number_of_reasons == 1:
        return "MEDIUM"

    return "LOW"


def main():

    if not os.path.exists(INPUT_FILE):

        print(
            "live_results.csv not found."
        )

        return

    df = pd.read_csv(INPUT_FILE)

    if df.empty:

        print("No data available.")

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

        # ==============================
        # NEW ANOMALY
        # ==============================

        if (
            row["status"] == "ANOMALY"
            and not incident_active
        ):

            reasons = explain_anomaly(
                row,
                previous_row
            )

            severity = calculate_severity(
                reasons
            )

            events.append({

                "timestamp":
                    row["timestamp"],

                "event_type":
                    "NEW_ANOMALY",

                "severity":
                    severity,

                "description":
                    " | ".join(reasons)
            })

            incident_active = True

        # ==============================
        # RECOVERY
        # ==============================

        elif (
            row["status"] == "NORMAL"
            and incident_active
        ):

            events.append({

                "timestamp":
                    row["timestamp"],

                "event_type":
                    "RECOVERY",

                "severity":
                    "INFO",

                "description":
                    "Server returned to normal behavior"
            })

            incident_active = False

    events_df = pd.DataFrame(events)

    events_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\n==============================")
    print("ANOMALY EXPLANATION COMPLETE")
    print("==============================")

    print(
        "Events detected:",
        len(events_df)
    )

    if not events_df.empty:

        print(
            events_df.to_string(
                index=False
            )
        )


if __name__ == "__main__":
    main()