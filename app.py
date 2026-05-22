import streamlit as st
import docker
from datetime import datetime

st.set_page_config(page_title="Homelab Guardian", layout="wide")
st.title("🏠 Homelab Guardian")
st.caption(f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# === CONFIGURATION ===
st.sidebar.header("Connection")
host_type = st.sidebar.radio("Monitor", ["Local Docker", "Remote Host (Future)"])

if host_type == "Local Docker":
    try:
        client = docker.from_env(timeout=5)
        containers = client.containers.list(all=True)
        st.sidebar.success(f"✅ Connected to local Docker ({len(containers)} containers)")
    except Exception as e:
        st.sidebar.error(f"Could not connect to Docker: {e}")
        containers = []
else:
    st.info("Remote multi-host monitoring coming in v1.1")
    containers = []

# Main Dashboard
col1, col2, col3 = st.columns(3)
col1.metric("Total Containers", len(containers))
running = len([c for c in containers if c.status == "running"])
col2.metric("Running", running)
col3.metric("Services", "12+")  # Update as needed

st.subheader("Service Status")

# Your actual services (add/remove as needed)
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
}

cols = st.columns(4)
i = 0
for display_name, name_pattern in services.items():
    status = "❌ Not Found"
    for c in containers:
        if name_pattern.lower() in c.name.lower():
            status = "🟢 Running" if c.status == "running" else f"🔴 {c.status.title()}"
            break
    with cols[i % 4]:
        st.metric(display_name, status)
    i += 1

st.subheader("All Docker Containers")
if containers:
    data = [{"Name": c.name, "Status": c.status.title(), "Image": c.image.tags[0] if c.image.tags else "N/A"} for c in containers]
    st.dataframe(data, use_container_width=True)
else:
    st.info("No containers detected. Make sure Docker is running on this machine.")

st.caption("Built by Jason Ray • Phase 1: Single Host Monitoring")
