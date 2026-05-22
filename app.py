import streamlit as st
from datetime import datetime
import docker
from pathlib import Path

st.set_page_config(page_title="Homelab Guardian", layout="wide")
st.title("🏠 Homelab Guardian")
st.caption(f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Sidebar
st.sidebar.header("Homelab Overview")
st.sidebar.success("Connected to Docker")

# Main sections
col1, col2, col3 = st.columns(3)
col1.metric("Docker Containers", "18", "2 running")
col2.metric("Media Library Size", "12.4 TB", "-87 GB")
col3.metric("Active Services", "14", "✅ All good")

st.subheader("Service Status")

# Example service cards - we'll expand this
services = {
    "Jellyfin": "🟢 Running",
    "Radarr": "🟢 Running",
    "Sonarr": "🟢 Running",
    "Lidarr": "🟢 Running",
    "Nextcloud": "🟢 Running",
    "Home Assistant": "🟢 Running",
    "Paperless": "🟢 Running",
    "Unmanic": "🟡 Processing",
}

cols = st.columns(4)
i = 0
for name, status in services.items():
    with cols[i % 4]:
        st.metric(name, status)
    i += 1

st.subheader("Storage")
st.info("Storage overview coming in next update...")

st.caption("Built by Jason Ray • Companion to other homelab and MECM tools")
