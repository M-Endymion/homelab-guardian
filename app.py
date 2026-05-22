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
    st.error("No config.json found. Please create one.")

# Sidebar - Host Selection
st.sidebar.header("Monitor Host")
host_options = ["Local Docker"] + [h["name"] for h in config.get("hosts", [])]
selected_host_name = st.sidebar.selectbox("Select Host", host_options, index=0)

containers = []

if selected_host_name == "Local Docker":
    try:
        client = docker.from_env(timeout=10)
        containers = client.containers.list(all=True)
        st.sidebar.success(f"✅ Local Docker ({len(containers)} containers)")
    except Exception as e:
        st.sidebar.error(f"Local Docker connection failed: {str(e)[:80]}")
else:
    # Find host config
    host_config = next((h for h in config.get("hosts", []) if h["name"] == selected_host_name), None)
    
    if host_config:
        st.sidebar.info(f"Connecting to {host_config['host']} via SSH...")
        
        try:
            # SSH Connection
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            if "key_path" in host_config:
                ssh.connect(
                    hostname=host_config["host"],
                    username=host_config["user"],
                    key_filename=host_config["key_path"],
                    port=host_config.get("port", 22),
                    timeout=10
                )
            else:
                ssh.connect(
                    hostname=host_config["host"],
                    username=host_config["user"],
                    password=host_config.get("password"),
                    port=host_config.get("port", 22),
                    timeout=10
                )
            
            # Execute docker command over SSH
            stdin, stdout, stderr = ssh.exec_command("docker ps -a --format '{{json .}}'")
            output = stdout.read().decode()
            
            # Parse output into container list
            containers = []
            for line in output.strip().split('\n'):
                if line:
                    try:
                        c = json.loads(line)
                        containers.append(type('obj', (object,), {
                            'name': c.get('Names', ''),
                            'status': c.get('Status', '').split()[0],
                            'image': c.get('Image', '')
                        }))
                    except:
                        pass
            
            st.sidebar.success(f"✅ Connected to {selected_host_name} ({len(containers)} containers)")
            
        except Exception as e:
            st.sidebar.error(f"SSH Connection failed: {str(e)[:100]}")
            containers = []

# === Dashboard Content (same as before) ===
col1, col2, col3 = st.columns(3)
col1.metric("Total Containers", len(containers))
running = len([c for c in containers if getattr(c, 'status', '') == "running"])
col2.metric("Running", running)
col3.metric("Host", selected_host_name)

st.subheader("Service Status")

# (Keep your common_services dictionary from before)

st.caption("Built by Jason Ray • Multi-host monitoring via SSH")
