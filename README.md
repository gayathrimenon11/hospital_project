
# Hospital Queue Management System 🏥

A full-stack Python application built for hospital workflows. Receptionists can check in incoming patients, and doctors can manage live consultation queues.

---

## 🛠️ Project Architecture & Tech Stack

* **Backend API:** FastAPI (Async Python framework) + Uvicorn (ASGI web server) + Pydantic (Data validation)
* **Frontend UI:** Streamlit
* **Dependency & Environment Management:** `uv` (Fast Python package manager)
* **Version Control:** Git & GitHub

---

## 📋 Prerequisites

Make sure you have `uv` and `git` installed on your machine:
* Verify `uv`: `uv --version`
* Verify `git`: `git --version`

---

## 📁 Project Setup Commands

Run these commands inside your `hospital_project` folder:

```shell

# Initialize uv project configuration
uv init

# Install dependencies into local .venv environment
uv add fastapi uvicorn streamlit requests pydantic

```

---

## ⚡ How to Run the Application

Open **two separate terminal windows** in VS Code inside your `hospital_project` folder:

### Terminal 1: Launch Backend API (FastAPI)

```shell
uv run uvicorn src.hospital_project.main:app --reload

```

* **Interactive API Documentation:** `http://127.0.0.1:8000/docs`

### Terminal 2: Launch Frontend UI (Streamlit)

```shell
uv run streamlit run src\hospital_project\app.py

```

* **Live Web Interface:** `http://localhost:8501`

---

## 🐙 Git & GitHub Commands

### 1. First-Time Repository Setup & Initial Push

```shell
# Initialize repository
git init

# Stage and commit files
git add .
git commit -m "Initial commit: Hospital queue system with FastAPI and Streamlit"

# Rename branch to main
git branch -M main

# Link remote GitHub repository
git remote add origin [https://github.com/gayathrimenon11/hospital_project.git](https://github.com/gayathrimenon11/hospital_project.git)

# Push code to GitHub
git push -u origin main

```

---

### 2. Daily Workflow: Saving & Pushing Future Changes

```shell
# Check current status
git status

# Stage all updated files
git add .

# Create commit with descriptive message
git commit -m "feat: add new feature or fix"

# Push updates to GitHub
git push origin main

```

---

### 3. Fresh Reset & Force Push (Clear Local History)

If you need to wipe local commits and push a clean single commit to GitHub:

```shell
# Remove existing git tracking history
Remove-Item -Recurse -Force .git

# Re-initialize and commit
git init
git add .
git commit -m "Initial commit: Hospital queue management system"

# Configure branch and remote link
git branch -M main
git remote add origin [https://github.com/gayathrimenon11/hospital_project.git](https://github.com/gayathrimenon11/hospital_project.git)

# Force push to overwrite remote history on GitHub
git push -u origin main --force

```

---

## 📄 Recommended `.gitignore` File

Create a file named `.gitignore` in your root folder with the following content:

```gitignore
# Virtual Environment
.venv/

# Python Cache
__pycache__/
*.pyc

# Streamlit Local Configurations
.streamlit/

# Environment Variables
.env

```