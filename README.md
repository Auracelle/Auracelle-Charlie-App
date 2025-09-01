# Auracelle Charlie – AI Governance Simulation Sandbox

This repository contains the **Auracelle Charlie** Streamlit application for simulating AI governance policies between countries and entities using reinforcement learning and influence mapping.

## 💻 Features

- Two-page app: Captive Login → Simulation Interface
- Select Country A/B, roles, and policy scenarios
- Alignment scoring, Q-learning policy negotiation
- Influence network graph + geo intelligence map
- Azure-compatible GitHub Actions deployment

## 🚀 Deployment on Azure

1. Ensure `AZURE_WEBAPP_PUBLISH_PROFILE` or client credentials are set in GitHub Secrets.
2. Push changes to the `main` branch.
3. GitHub Actions auto-deploys via `.github/workflows/Azure-Deploy.yml`.

## 📁 Structure

```
.
├── app.py
├── pages/
│   └── auracelle_charlie_simulation.py
├── requirements.txt
├── .github/workflows/
│   └── Azure-Deploy.yml
└── README.md
```

---

MIT License © 2025 Grace-Alice Evans
