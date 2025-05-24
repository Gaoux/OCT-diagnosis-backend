# 📦 OCT-Diagnosis-Backend

## 🧠 Overview

OCT-Diagnosis-Backend is a Django-based backend for an Optical Coherence Tomography (OCT) diagnostic system. This backend provides RESTful API endpoints to handle image uploads, process medical images, and return AI-driven diagnostic insights.

## ✨ Features

- Image upload and preprocessing
- Deep learning model inference for classification
- User authentication and role-based access
- Database for storing diagnostic results
- API endpoints following RESTful architecture

## 🚀 Installation & Development with Docker Compose

This project uses Docker Compose for development and deployment.

### 🐳 What Docker Compose Does

- Sets up a Django backend (`web` service)
- Sets up a PostgreSQL database (`db` service)
- Links both containers via a shared network
- Mounts local project files into the container
- Exposes Django at [http://localhost:8000](http://localhost:8000)

### 📁 How to Set It Up

#### 1. Clone the Repository

```bash
git clone https://github.com/gaoux/OCT-diagnosis-backend.git
cd OCT-diagnosis-backend
```

#### 2. Create a `.env` file

You can copy the provided `.env.example`:

```bash
cp .env.example .env
```

Or manually create your own `.env` with the structure of the `env.example` file.

#### 3. Build the Docker Images

```bash
docker-compose build --no-cache
```

#### 4. Run the Project

```bash
docker-compose up
```

Django will be available at:  
[http://localhost:8000](http://localhost:8000)

### 🧹 Clean Up (Remove Volumes and Containers)

To stop and clean the environment, including database volumes:

```bash
docker-compose down -v
```

> ⚠️ Warning: This will delete all PostgreSQL data.

---

## 📦 Keeping Dependencies Up to Date

If you or any team member installs or modifies dependencies inside the environment, they must update the `requirements.txt` file with:

```bash
pip freeze | grep -vE ' @ file://|^-e|pywin32|win32|colorama|pypiwin32|tensorflow-intel' > requirements.txt
```

This ensures clean, cross-platform, Docker-friendly dependencies.

---

## 📂 Project Structure

- `docker-compose.yml`: Defines services for Django and PostgreSQL
- `requirements.txt`: pip dependencies
- `environment.yml`: Defines the Conda environment (only if working outside Docker)
- `manage.py`, `settings.py`: Django backend
- `.env`: Environment variables for DB and Django setup

---

## 🧠 AI Model Integration

The backend integrates a deep learning model to classify OCT (Optical Coherence Tomography) images into four diagnostic categories. This model is based on a Keras-compatible architecture (e.g., Xception), trained to assist in ophthalmological pre-diagnosis.


## 📬 API Endpoints

### 👤 User Endpoints

| Method | Endpoint                     | Description                  |
| ------ | ---------------------------- | ---------------------------- |
| POST   | `/api/users/register/`       | Register a new user          |
| POST   | `/api/users/login/`          | Log in and obtain JWT token  |
| POST   | `/api/users/reset-password/` | Reset password using a token |

---

### 🛡️ Admin Endpoints

| Method | Endpoint                 | Description                       |
| ------ | ------------------------ | --------------------------------- |
| POST   | `/api/users/register/`   | Register a new user               |
| GET    | `/api/users/users/`      | List all users                    |
| GET    | `/api/users/users/<id>/` | Get user details                  |
| PATCH  | `/api/users/users/<id>/` | Update user information           |
| DELETE | `/api/users/users/<id>/` | Delete a user                     |
| POST   | `/api/oct/upload-model/` | Upload or replace the `.h5` model |

---

### 📄 Report Endpoints

| Method | Endpoint                         | Description                             |
| ------ | -------------------------------- | --------------------------------------- |
| POST   | `/api/reports/create/`           | Create a new report                     |
| GET    | `/api/reports/history/`          | List reports for the authenticated user |
| GET    | `/api/reports/`                  | List all reports (admin only)           |
| GET    | `/api/reports/<uuid:id>/`        | Get report details                      |
| PATCH  | `/api/reports/<uuid:id>/update/` | Update report comments                  |
| DELETE | `/api/reports/<uuid:id>/delete/` | Delete a report                         |
| GET    | `/api/reports/<uuid:id>/image/`  | Download image associated with a report |
| GET    | `/api/reports/summary/`          | Get summary of reports (statistics)     |

---

### 🤖 AI Prediction Endpoint

| Method | Endpoint            | Description                    |
| ------ | ------------------- | ------------------------------ |
| POST   | `/api/oct/predict/` | Run prediction on an OCT image |

> **Note:** All endpoints (except login, register and reset-password) require JWT authentication.

---

## 📝 License

This project is licensed under the GPL-3.0 license.
