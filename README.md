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
git clone https://github.com/gaoux/OCT-diagnosis-backend.git
cd OCT-diagnosis-backend
```

### 2. Setup Environment with Conda

Ensure you have [Conda installed](https://docs.conda.io/en/latest/miniconda.html).

#### Create the Conda Environment

```bash
conda env create -f environment.yml
```

#### Activate the Environment

```bash
conda activate octenv
```

> ℹ️ The environment name is defined in `environment.yml`. If you want to rename it, change the `name:` field in the file.

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
[http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## API Endpoints

Coming soon...

---

## Updating Dependencies

If you install new packages in the environment, you can update the `environment.yml` file:

```bash
conda env export --from-history > environment.yml
```

---

## License

This project is licensed under the GPL-3.0 license.

```

```
