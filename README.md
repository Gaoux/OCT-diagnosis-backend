# OCT-Diagnosis-Backend

## Overview

OCT-Diagnosis-Backend is a Django-based backend for an Optical Coherence Tomography (OCT) diagnostic system. This backend provides RESTful API endpoints to handle image uploads, process medical images, and return AI-driven diagnostic insights.

## Features

- Image upload and preprocessing
- Deep learning model inference for classification
- User authentication and role-based access
- Database for storing diagnostic results
- API endpoints following RESTful architecture

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/gaoux/OCT-diagnosis-backend.git`
cd OCT-diagnosis-backend `
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Apply Migrations

```bash
python manage.py migrate
```

### 4. Create a Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 5. Run the Development Server

```bash
python manage.py runserver
```

The API should now be accessible at:
http://127.0.0.1:8000

### Create and Activate a Virtual Environment (Conda)

```bash
conda create -n oct_backend_env python=3.9
conda activate oct_backend_env
```

## API Endpoints

Coming soon...

## License

This project is licensed under the GPL-3.0 license.
