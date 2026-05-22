import streamlit as st
import docker
from datetime import datetime
from pathlib import Path

st.set_page_config(page_title="Homelab Guardian", layout="wide")
st.title("🏠 Homelab Guardian")
st.caption(f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Connect to Docker
try:
    client = docker.from_env()
    containers = client.containers.list(all=True)
    st.sidebar.success(f"Connected to Docker ({len(containers)} containers)")
except Exception as e:
    st.sidebar.error("Could not connect to Docker. Is Docker running?")
    containers = []

# Main metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Containers", len(containers))
running = len([c for c in containers if c.status == "running"])
col2.metric("Running", running, f"{running - len(containers)} stopped")
col3.metric("Services Monitored", "12")
col4.metric("Storage", "N/A", "Coming soon")

st.subheader("Service Status")

# Define your actual services
services = {
    "Jellyfin": "jellyfin",
    "Radarr": "radarr",
    "Sonarr": "sonarr",
    "Lidarr": "lidarr",
    "Nextcloud": "nextcloud",
    "Home Assistant": "homeassistant",
    "Paperless": "paperless",
    "Unmanic": "unmanic",
    "Navidrome": "navidrome",
    "Ryot": "ryot",
    # Add more as needed
}

cols = st.columns(4)
i = 0
for display_name, container_name in services.items():
    status = "❌ Not Found"
    color = "red"
    
    for c in containers:
        if container_name.lower() in c.name.lower():
            if c.status == "running":
                status = "🟢 Running"
                color = "green"
            else:
                status = f"🔴 {c.status.title()}"
            break
    
    with cols[i % 4]:
        st.metric(display_name, status)
    i += 1

st.subheader("Docker Containers")
if containers:
    data = []
    for c in containers:
        data.append({
            "Name": c.name,
            "Status": c.status,
            "Image": c.image.tags[0] if c.image.tags else "N/A",
            "Uptime": "N/A"
        })
    st.dataframe(data, use_container_width=True)
else:
    st.info("No containers found.")

st.caption("Built by Jason Ray • Real-time homelab monitoring")
