import streamlit as st
import docker
from datetime import datetime

st.set_page_config(page_title="Homelab Guardian", layout="wide")
st.title("🏠 Homelab Guardian")
st.caption(f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Connect to Docker
try:
    client = docker.from_env(timeout=8)
    containers = client.containers.list(all=True)
    st.sidebar.success(f"✅ Connected to Docker ({len(containers)} containers)")
except Exception as e:
    st.sidebar.error(f"Could not connect to Docker: {str(e)[:100]}...")
    containers = []

# Main Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Containers", len(containers))
running = len([c for c in containers if c.status == "running"])
col2.metric("Running", running, f"{len(containers) - running} stopped")
col3.metric("Services", len(containers))

st.subheader("Service Status")

# More dynamic service detection (partial name matching)
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
    "Homarr": ["homarr"],
    "Heimdall": ["heimdall"],
    "Tautulli": ["tautulli"],
    "Portainer": ["portainer"],
    "Linkding": ["linkding"],
    "Piwigo": ["piwigo"],
}

cols = st.columns(4)
i = 0
for display_name, keywords in common_services.items():
    status = "❌ Not Found"
    for c in containers:
        if any(kw.lower() in c.name.lower() for kw in keywords):
            if c.status == "running":
                status = "🟢 Running"
            else:
                status = f"🔴 {c.status.title()}"
            break
    with cols[i % 4]:
        st.metric(display_name, status)
    i += 1

st.subheader("All Docker Containers")
if containers:
    data = []
    for c in containers:
        data.append({
            "Name": c.name,
            "Status": c.status.title(),
            "Image": c.image.tags[0] if c.image.tags else c.image.id[:12]
        })
    st.dataframe(data, use_container_width=True)
else:
    st.info("No containers detected.")

st.caption("Built by Jason Ray • Dynamic service detection")
