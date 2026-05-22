import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import paramiko
import docker

st.set_page_config(page_title="Homelab Guardian", layout="wide")
st.title("🏠 Homelab Guardian")
st.caption(f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Load config
config_path = Path("config.json")
if config_path.exists():
    with open(config_path) as f:
        config = json.load(f)
else:
    config = {"hosts": []}
    st.warning("No config.json found. Create one to add remote hosts.")

# Sidebar - Host Selection
st.sidebar.header("Hosts")
selected_host = st.sidebar.selectbox(
    "Select Host to Monitor",
    options=["Local Docker"] + [h["name"] for h in config["hosts"]],
    index=0
)

containers = []

if selected_host == "Local Docker":
    try:
        client = docker.from_env(timeout=8)
        containers = client.containers.list(all=True)
        st.sidebar.success(f"✅ Local Docker ({len(containers)} containers)")
    except:
        st.sidebar.error("Could not connect to local Docker")
else:
    # Find selected host config
    host_config = next((h for h in config["hosts"] if h["name"] == selected_host), None)
    if host_config:
        st.sidebar.info(f"Connecting to {host_config['host']}...")
        # SSH + Docker connection logic (simplified for now)
        st.info(f"Remote monitoring for {selected_host} coming in next update (SSH + Docker over socket)")
        containers = []  # Placeholder

# Rest of dashboard (same as before)
col1, col2, col3 = st.columns(3)
col1.metric("Total Containers", len(containers))
running = len([c for c in containers if c.status == "running"])
col2.metric("Running", running)
col3.metric("Host", selected_host)

# ... (rest of service status and container list from previous version)

st.caption("Built by Jason Ray • Multi-host support in progress")
