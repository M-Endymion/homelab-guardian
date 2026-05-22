import streamlit as st
import docker
import psutil
from datetime import datetime
import time

st.set_page_config(page_title="Homelab Guardian", layout="wide")
st.title("🏠 Homelab Guardian")
st.caption(f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Docker Connection
try:
    client = docker.from_env(timeout=10)
    containers = client.containers.list(all=True)
    st.sidebar.success(f"✅ Connected to Docker ({len(containers)} containers)")
except Exception as e:
    st.sidebar.error(f"❌ Docker connection failed: {str(e)[:100]}")
    containers = []

# Storage
st.sidebar.header("Storage")
for partition in psutil.disk_partitions():
    if partition.mountpoint in ['/', '/mnt', '/data']:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            st.sidebar.metric(f"{partition.mountpoint}", f"{usage.percent}%", f"{round(usage.free/(1024**3),1)} GB free")
        except:
            pass

# Main Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Containers", len(containers))
running = len([c for c in containers if c.status == "running"])
col2.metric("Running", running, f"{len(containers)-running} stopped")
col3.metric("Services", "18+")
col4.metric("Uptime", "N/A")   # Can be improved later

st.subheader("Service Status")

# Expanded service list with better matching
common_services = {
    "Jellyfin": ["jellyfin"],
    "Radarr": ["radarr"],
    "Sonarr": ["sonarr"],
    "Lidarr": ["lidarr"],
    "Nextcloud": ["nextcloud"],
    "Home Assistant": ["homeassistant", "hass"],
    "Paperless": ["paperless"],
    "Unmanic": ["unmanic"],
    "Navidrome": ["navidrome"],
    "Photoprism": ["photoprism"],
    "Photoview": ["photoview"],
    "Homarr": ["homarr"],
    "Heimdall": ["heimdall"],
    "Tautulli": ["tautulli"],
    "Portainer": ["portainer"],
    "Linkding": ["linkding"],
    "Piwigo": ["piwigo"],
    "Ryot": ["ryot"],
    "Mealie": ["mealie"],
    "OnlyOffice": ["onlyoffice"],
}

cols = st.columns(4)
i = 0
for display_name, keywords in common_services.items():
    status = "❌ Not Found"
    for c in containers:
        if any(kw.lower() in c.name.lower() for kw in keywords):
            status = "🟢 Running" if c.status == "running" else f"🔴 {c.status.title()}"
            break
    with cols[i % 4]:
        st.metric(display_name, status)
    i += 1

st.subheader("All Docker Containers")
if containers:
    data = [{
        "Name": c.name,
        "Status": c.status.title(),
        "Image": c.image.tags[0] if c.image.tags else c.image.id[:12],
        "Created": c.attrs['Created'][:10]
    } for c in containers]
    st.dataframe(data, use_container_width=True)
else:
    st.info("No containers found.")

# Refresh button
if st.button("🔄 Refresh Now"):
    st.rerun()

st.caption("Built by Jason Ray • Dynamic service detection")
