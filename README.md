# 📋 Customer Feedback Board (Demo App)

A lightweight Python Flask application built to showcase the **Terraform Developer Portal**. It morphs its UI natively using environment flags passed from the portal lifecycle.

## 🛠️ Environment API

| Variable | Value | Description |
| :--- | :--- | :--- |
| `AI_ENABLED` | `true` | Day 1 Add-on: Displays sentiment color badges. |
| `MAINTENANCE_MODE` | `true` | Day 2 Action: Displays a 503 maintenance splash. |

## 🚀 Quick Run (Local Testing)
```bash
export AI_ENABLED=true
export MAINTENANCE_MODE=false
python app.py
```

## 🐳 Docker Build
```bash
docker build -t feedback-app:latest .
```
