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

Copy or create a `.env` file with the following:

```env
# Database Configuration
DB_NAME=oct_sense
DB_USER=django_user
DB_PASSWORD=securepassword123
DB_HOST=db
DB_PORT=5432

# PostgreSQL Configuration
POSTGRES_DB=oct_sense
POSTGRES_USER=django_user
POSTGRES_PASSWORD=securepassword123

# JWT
SECRET_KEY=your-super-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

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
- `environment.yml`: Defines the Conda environment (used only if working outside Docker)
- `manage.py`, `settings.py`: Django backend
- `.env`: Environment variables for DB and Django setup

---

## 📬 API Endpoints

Coming soon...

---

## 📝 License

This project is licensed under the GPL-3.0 license.
