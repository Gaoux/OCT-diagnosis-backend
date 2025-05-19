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
Or manually create your own .env with the structure of the `env.example` file.

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
## 🧠 IA Model Integration

The backend integrates a deep learning model to classify OCT (Optical Coherence Tomography) images into four diagnostic categories. This model is based on a Keras-compatible architecture (e.g., Xception), trained to assist in ophthalmological pre-diagnosis.

## 📦 Model Requirements 

To ensure compatibility with the system, any model uploaded for the first time must meet the following criteria:

- ✅ **Format:** The model file must be in `.h5` format (Keras HDF5).  
- ✅ **Input Shape:** It must accept input images of size **(299, 299, 3)**.  
- ✅ **Output Layer:** The output must have **4 neurons** with **softmax** activation for multi-class classification.  
- ✅ **Loss Function:** The model must be trained using **categorical_crossentropy**.  
- ✅ **Class Order:** The prediction outputs must correspond **exactly** to the following order:
["CNV", "DME", "DRUSEN", "NORMAL"]

### 🆕 Initial Model Upload

To upload the model for the first time:

1. Ensure the model complies with all the above requirements.
2. Place the `.h5` file in the directory `apps/oct_analysis/model/`.
3. Verify the file name is exactly oct_model.h5
4. Start the backend container with Docker

## 📬 API Endpoints

### 👤 Endpoints para Usuarios

| Método | Endpoint                                 | Descripción                                         |
|--------|------------------------------------------|-----------------------------------------------------|
| POST   | `/api/users/register/`                   | Registrar un nuevo usuario                          |
| POST   | `/api/users/login/`                      | Iniciar sesión y obtener token JWT                  |
| POST   | `/api/users/reset-password/`             | Restablecer contraseña con token                    |
---

### 🛡️ Endpoints para Administradores

| Método | Endpoint                                 | Descripción                                         |
|--------|------------------------------------------|-----------------------------------------------------|
| POST   | `/api/users/register/`                   | Registrar un nuevo usuario                          |
| GET    | `/api/users/users/`                      | Listar todos los usuarios                           |
| GET    | `/api/users/users/<id>/`                 | Obtener detalles de un usuario                      |
| PATCH  | `/api/users/users/<id>/`                 | Editar usuario                                      |
| DELETE | `/api/users/users/<id>/`                 | Eliminar usuario                                    |
| POST   | `/api/oct/upload-model/`                 | Subir o reemplazar el modelo `.h5`                  |

---
### 📄 Endpoints para Reportes

| Método | Endpoint                                   | Descripción                                         |
|--------|--------------------------------------------|-----------------------------------------------------|
| POST   | `/api/reports/create/`                     | Crear un nuevo reporte                              |
| GET    | `/api/reports/history/`                    | Listar reportes del usuario autenticado             |
| GET    | `/api/reports/`                            | Listar todos los reportes (admin)                   |
| GET    | `/api/reports/<uuid:id>/`                  | Obtener detalles de un reporte                      |
| PATCH  | `/api/reports/<uuid:id>/update/`           | Actualizar comentarios de un reporte                |
| DELETE | `/api/reports/<uuid:id>/delete/`           | Eliminar un reporte                                 |
| GET    | `/api/reports/<uuid:id>/image/`            | Descargar imagen asociada a un reporte              |
| GET    | `/api/reports/summary/`                    | Obtener resumen de reportes (estadísticas)          |

---
### 🤖 Modelo de IA

| Método | Endpoint                      | Descripción                                         |
|--------|-------------------------------|-----------------------------------------------------|
| POST   | `/api/oct/predict/`           | Realizar predicción sobre una imagen OCT            |

> **Nota:** Todos los endpoints (excepto login y reset-password) requieren autenticación mediante token JWT.



---

## 📝 License

This project is licensed under the GPL-3.0 license.
