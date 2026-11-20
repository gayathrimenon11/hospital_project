
# Hospital Queue Management System 🏥

A full-stack Python application built for hospital workflows. Receptionists can check in incoming patients, and doctors can manage live consultation queues.

---

## 🛠️ Project Architecture & Tech Stack

* **Frontend UI:** Streamlit (in `frontend/`)
* **Backend API:** FastAPI + Uvicorn + Pydantic (in `backend/`)
* **Database:** PostgreSQL 16 + SQLAlchemy ORM
* **Containerization:** Docker & Docker Compose
* **Package Management:** `uv`
* **Version Control:** Git & GitHub

---

## ⚡ How to Run with Docker (Recommended)

Make sure [Docker Desktop](https://www.docker.com/products/docker-desktop/) is running, then run:

```shell
docker-compose up --build
```

- **Frontend (Streamlit UI):** [http://localhost:8501](http://localhost:8501)
- **Backend API & Swagger Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Database (PostgreSQL):** Running on port `5432` with data persisted in the `postgres_data` volume.

To stop the containers:
```shell
docker-compose down
```

---

## 💻 Local Development (Without Docker)

### 1. Backend
```shell
cd backend
uv run uvicorn src.main:app --reload --port 8000
```

### 2. Frontend
```shell
cd frontend
uv run streamlit run src/app.py --server.port 8501
```

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