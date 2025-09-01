# 🚀 Auracelle Charlie — Azure Deployment via GitHub Actions

This repository is configured to deploy **Auracelle Charlie** directly to **Azure Web App** using a secure GitHub Actions workflow and OpenID Connect (OIDC) authentication.

## 📂 Deployment File

- `.github/workflows/Azure-Deploy.yml`: Main GitHub Actions workflow that builds and deploys the app to Azure.

## ✅ Setup Prerequisites

1. **Azure Web App** created for Python 3.11.
2. **OIDC Authentication** secrets added in GitHub repository:
   - `AZUREAPPSERVICE_CLIENTID_CA59A126D6FF447D91D44D0AA0D30FD9`
   - `AZUREAPPSERVICE_TENANTID_9712D91B25E5481C99C3C19B858946D5`
   - `AZUREAPPSERVICE_SUBSCRIPTIONID_D3CDEDF6E2B04C1D8B3A217DF516CD1A`

## 🚦 How it Works

- **On Push to `main`** or Manual Trigger:
  - Creates a virtual environment
  - Installs requirements
  - Uploads project files as artifact
  - Logs in to Azure securely using OIDC
  - Deploys using `azure/webapps-deploy@v3`

## 📁 Repository Structure

```
📦 Auracelle-Charlie
 ┣ 📁 pages/
 ┣ 📄 app.py
 ┣ 📄 requirements.txt
 ┣ 📄 .github/workflows/Azure-Deploy.yml
 ┗ 📄 README.md
```

For help, contact Grace-Alice Evans or the AGPO DevOps team.
