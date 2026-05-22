<div align="center">
  <img src="https://raw.githubusercontent.com/M-Endymion/homelab-guardian/main/thumbnail.png" alt="Homelab Guardian" width="100%" />
</div>

<br>

# Homelab Guardian

A clean, real-time **Streamlit dashboard** to monitor my homelab at a glance.

Built for a Proxmox + Docker environment running Jellyfin, *arr stack, Nextcloud, Home Assistant, and many other services.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

---

## Features

- Real-time Docker container status
- Dynamic service detection (Jellyfin, Radarr, Sonarr, Nextcloud, etc.)
- Storage usage overview
- Clean, responsive interface
- Easy to extend with more metrics

---

## Screenshots

![Homelab Guardian Dashboard](https://raw.githubusercontent.com/M-Endymion/homelab-guardian/main/screenshots/dashboard.png)

---

## Quick Start

```bash
git clone https://github.com/M-Endymion/homelab-guardian.git
cd homelab-guardian
pip install -r requirements.txt
streamlit run app.py
```

Or use the helper script:
```bash
./run.sh
```

---

## Current Capabilities

- Shows all Docker containers with status and image
- Highlights key services with color-coded status
- Storage metrics
- Works on any Docker host (including remote via SSH tunnel)

---

## Future Plans

- Multi-host monitoring (multiple Proxmox VMs)
- Proxmox API integration (VM list, CPU/RAM per host)
- Media library stats (Jellyfin item count, *arr queue status)
- Alerting and notifications
- Historical graphs

---

**Jason Ray (M-Endymion)**

MECM/SCCM Automation + Homelab Enthusiast

- **LinkedIn:** Jason Ray
- **Main Portfolio:** m-endymion.github.io
- **GitHub:** github.com/M-Endymion

**Last Updated:** May 2026
