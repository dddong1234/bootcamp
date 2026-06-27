import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="Adbrix Style Dashboard")

# Custom CSS to mimic the Adbrix UI (sidebar, colors, padding)
st.markdown("""
    <style>
    /* Background and padding */
    .main {
        background-color: #f4f7f9;
    }
    .stApp {
        background-color: #f4f7f9;
    }

    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #e1e4e8;
        padding: 15px;
        border-radius: 5px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    /* Header Styling */
    h3 {
        color: #444;
        font-size: 1.1rem !important;
        margin-bottom: 10px !important;
    }

    /* Navigation Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar Implementation
with st.sidebar:
    st.image("https://www.adbrix.ai/assets/images/common/logo.png", width=120)  # Adbrix Logo Placeholder
    st.markdown("---")
    st.button("🏠 Dashboard", use_container_width=True)
    st.button("📈 Analytics", use_container_width=True)
    st.button("🔗 Attributions", use_container_width=True)
    st.button("👥 Audience", use_container_width=True)
    st.button("📂 Export Data", use_container_width=True)
    st.button("⚙️ Setting & SDK", use_container_width=True)
    st.markdown("---")
    st.info("Demo User\nUTC+9")


# 3. Sample Data Generation
@st.cache_data
def get_mock_data():
    channels = ['Google', 'Facebook', 'Twitter', 'Organic', 'Tradingworks']
    dates = pd.date_range(end=datetime.today(), periods=7)

    data = []
    for date in dates:
        for channel in channels:
            data.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Channel": channel,
                "New Install": np.random.randint(1000, 5000),
                "Daily Revenue": np.random.randint(50000, 200000),
                "App Open": np.random.randint(5000, 15000),
                "Re-open": np.random.randint(1000, 3000)
            })
    return pd.DataFrame(data)


df = get_mock_data()

# 4. Header Section
col_head1, col_head2 = st.columns([8, 2])
with col_head1:
    st.title("⬅ Dashboard")
with col_head2:
    st.button("편집 취소")
    st.button("편집 완료", type="primary")

# 5. Row 1: KPI Metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("New Install by Ad Channel", "14,444", "-823", delta_color="inverse")
m2.metric("Daily Revenue", "424.057", "-6,119", delta_color="inverse")
m3.metric("Revenue (iOS)", "424.857", "+25,534")
m4.metric("Revenue (Total)", "14,842", "-1,023", delta_color="inverse")

st.markdown("<br>", unsafe_allow_html=True)

# 6. Row 2: Charts (Pie & Table)
col1, col2 = st.columns([4, 6])

with col1:
    st.subheader("App Open by Ad Channel")
    fig_pie = px.pie(df.groupby("Channel")["App Open"].sum().reset_index(),
                     values='App Open', names='Channel',
                     color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_pie.update_layout(showlegend=True, margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.subheader("App Open by Ad Channel (Data)")
    table_df = df.groupby("Date").sum()[["New Install", "App Open", "Re-open"]]
    st.table(table_df.sort_index(ascending=False))

# 7. Row 3: Trends (Area & Bar)
col3, col4 = st.columns(2)

with col3:
    st.subheader("Daily App Open Trend")
    fig_area = px.area(df, x="Date", y="App Open", color="Channel",
                       color_discrete_sequence=px.colors.qualitative.Set3)
    fig_area.update_layout(margin=dict(t=10, b=10, l=10, r=10))
    st.plotly_chart(fig_area, use_container_width=True)

with col4:
    st.subheader("Channel Breakdown")
    fig_bar = px.bar(df.groupby("Channel")["Daily Revenue"].mean().reset_index(),
                     y="Channel", x="Daily Revenue", orientation='h',
                     color="Channel")
    st.plotly_chart(fig_bar, use_container_width=True)
