import streamlit as st
import pandas as pd
import plotly.express as px
import os

from streamlit_autorefresh import st_autorefresh


# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="Server Sentinel",
    page_icon="🖥️",
    layout="wide"
)

st_autorefresh(
    interval=5000,
    key="live_refresh"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0;
    }

    .subtitle {
        color: #888;
        font-size: 16px;
        margin-bottom: 25px;
    }

    .status-normal {
        padding: 15px;
        border-radius: 10px;
        background-color: #0f5132;
        color: white;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
    }

    .status-anomaly {
        padding: 15px;
        border-radius: 10px;
        background-color: #842029;
        color: white;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# HEADER
# ==========================================

st.markdown(
    '<div class="main-title">🖥️ Server Sentinel</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Machine Learning based real-time server monitoring'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================
# LOAD DATA
# ==========================================

live_file = "data/live_results.csv"

if not os.path.exists(live_file):

    st.warning(
        "Live monitor is not running."
    )

    st.code(
        "python src\\live_monitor.py"
    )

    st.stop()


df = pd.read_csv(live_file)

if df.empty:

    st.info(
        "Waiting for live server data..."
    )

    st.stop()


df["timestamp"] = pd.to_datetime(
    df["timestamp"]
)


latest = df.iloc[-1]


# ==========================================
# STATUS
# ==========================================

if latest["status"] == "ANOMALY":

    st.markdown(
        '<div class="status-anomaly">'
        '🚨 SERVER ANOMALY DETECTED'
        '</div>',
        unsafe_allow_html=True
    )

else:

    st.markdown(
        '<div class="status-normal">'
        '🟢 SERVER OPERATING NORMALLY'
        '</div>',
        unsafe_allow_html=True
    )


st.write("")


# ==========================================
# METRICS
# ==========================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "CPU",
        f"{latest['cpu_usage']:.1f}%"
    )


with col2:

    st.metric(
        "RAM",
        f"{latest['ram_usage']:.1f}%"
    )


with col3:

    st.metric(
        "Connections",
        int(latest["active_connections"])
    )


with col4:

    st.metric(
        "Response",
        f"{latest['response_time_ms']:.0f} ms"
    )


# ==========================================
# SUMMARY
# ==========================================

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Readings",
        len(df)
    )

with col2:
    st.metric(
        "Anomalies",
        int(
            (df["status"] == "ANOMALY").sum()
        )
    )

with col3:
    st.metric(
        "Latest Score",
        f"{latest['anomaly_score']:.4f}"
    )


# ==========================================
# CPU
# ==========================================

st.subheader("CPU Usage")

fig = px.line(
    df.tail(100),
    x="timestamp",
    y="cpu_usage"
)

fig.update_layout(
    xaxis_title="Time",
    yaxis_title="CPU %"
)

st.plotly_chart(
    fig,
    width="stretch"
)


# ==========================================
# RAM
# ==========================================

st.subheader("RAM Usage")

fig = px.line(
    df.tail(100),
    x="timestamp",
    y="ram_usage"
)

fig.update_layout(
    xaxis_title="Time",
    yaxis_title="RAM %"
)

st.plotly_chart(
    fig,
    width="stretch"
)


# ==========================================
# RESPONSE TIME
# ==========================================

st.subheader("Response Time")

fig = px.line(
    df.tail(100),
    x="timestamp",
    y="response_time_ms"
)

fig.update_layout(
    xaxis_title="Time",
    yaxis_title="Milliseconds"
)

st.plotly_chart(
    fig,
    width="stretch"
)


# ==========================================
# NETWORK
# ==========================================

st.subheader("Network Traffic")

network_df = df.tail(100)

fig = px.line(
    network_df,
    x="timestamp",
    y=[
        "bytes_sent_per_second",
        "bytes_received_per_second"
    ]
)

st.plotly_chart(
    fig,
    width="stretch"
)


# ==========================================
# INCIDENT HISTORY
# ==========================================

st.divider()

st.subheader("🚨 Incident History")

events_file = "data/events.csv"


if os.path.exists(events_file):

    events = pd.read_csv(
        events_file
    )

    if not events.empty:

        for _, event in events.tail(10).iloc[::-1].iterrows():

            if event["event_type"] == "NEW_ANOMALY":

                st.error(
                    f"🚨 {event['timestamp']} | "
                    f"{event['severity']} | "
                    f"{event['description']}"
                )

            else:

                st.success(
                    f"🟢 {event['timestamp']} | "
                    f"RECOVERED | "
                    f"{event['description']}"
                )

    else:

        st.info(
            "No incidents yet."
        )

else:

    st.info(
        "No event history available."
    )