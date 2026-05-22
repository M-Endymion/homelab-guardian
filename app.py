import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import paramiko

st.set_page_config(page_title="Homelab Guardian", layout="wide")
st.title("🏠 Homelab Guardian")
st.caption(f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Load config
config_path = Path("config.json")
config = json.load(open(config_path)) if config_path.exists() else {"hosts": []}

# Host Selection
st.sidebar.header("Monitor Host")
host_options = ["Local Docker"] + [h["name"] for h in config.get("hosts", [])]
selected_host_name = st.sidebar.selectbox("Select Host", host_options, index=0)

containers = []

if selected_host_name == "Local Docker":
    try:
        import docker
        client = docker.from_env(timeout=10)
        containers = client.containers.list(all=True)
        st.sidebar.success(f"✅ Local Docker ({len(containers)} containers)")
    except Exception as e:
        st.sidebar.error(f"Local Docker connection failed: {str(e)[:80]}")
else:
    host_config = next((h for h in config.get("hosts", []) if h["name"] == selected_host_name), None)
    if host_config:
        with st.spinner(f"Connecting to {selected_host_name}..."):
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                
                ssh.connect(
                    hostname=host_config["host"],
                    username=host_config["user"],
                    key_filename=host_config.get("key_path"),
                    port=host_config.get("port", 22),
                    timeout=15
                )
                
                # Get container list
                _, stdout, _ = ssh.exec_command("docker ps -a --format '{{.Names}}|{{.Status}}|{{.Image}}'")
                output = stdout.read().decode()
                
                containers = []
                for line in output.strip().split('\n'):
                    if line:
                        parts = line.split('|')
                        if len(parts) >= 3:
                            containers.append({
                                'name': parts[0],
                                'status': parts[1].split()[0].lower(),
                                'image': parts[2]
                            })
                
                st.sidebar.success(f"✅ Connected to {selected_host_name} ({len(containers)} containers)")
                ssh.close()
            except Exception as e:
                st.sidebar.error(f"Connection failed: {str(e)[:100]}")

# === Dashboard ===
col1, col2, col3 = st.columns(3)
col1.metric("Total Containers", len(containers))
running = len([c for c in containers if (isinstance(c, dict) and c.get('status') == "up") or (hasattr(c, 'status') and c.status == "running")])
col2.metric("Running", running)
col3.metric("Host", selected_host_name)

st.subheader("Service Status")

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
        name = c.get('name') if isinstance(c, dict) else getattr(c, 'name', '')
        if any(kw.lower() in name.lower() for kw in keywords):
            status_raw = c.get('status') if isinstance(c, dict) else getattr(c, 'status', '')
            status = "🟢 Running" if status_raw in ["up", "running"] else f"🔴 {status_raw.title()}"
            break
    with cols[i % 4]:
        st.metric(display_name, status)
    i += 1

st.subheader("All Docker Containers on this Host")
if containers:
    data = []
    for c in containers:
        if isinstance(c, dict):
            data.append({
                "Name": c.get('name', 'N/A'),
                "Status": c.get('status', 'N/A').title(),
                "Image": c.get('image', 'N/A')
            })
        else:
            data.append({
                "Name": getattr(c, 'name', 'N/A'),
                "Status": getattr(c, 'status', 'N/A').title(),
                "Image": getattr(c, 'image', 'N/A').tags[0] if getattr(c, 'image', None) else 'N/A'
            })
    st.dataframe(data, use_container_width=True)
else:
    st.info("No containers found on selected host.")

st.caption("Built by Jason Ray • Multi-host monitoring via SSH")
