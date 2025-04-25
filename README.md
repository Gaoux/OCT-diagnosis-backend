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

### 2. Setup Environment with Conda and pip

Ensure you have [Conda installed](https://docs.conda.io/en/latest/miniconda.html).

#### Create the Conda Environment

```bash
conda env create -f environment.yml
```

This will create an environment named `octsense` (or as defined in the `name:` field of `environment.yml`).

#### Activate the Environment

```bash
conda activate octsense
```

#### Install Python Dependencies via pip

Once inside the environment, install all dependencies listed in `requirements.txt`:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> ⚠️ All project dependencies must be installed using `pip`, not Conda.

---

## Keeping Dependencies Up to Date

If you or any team member installs or modifies dependencies inside the environment, they must update the `requirements.txt` file with:

```bash
pip freeze | grep -vE ' @ file://|^-e|pywin32|win32|colorama|pypiwin32|tensorflow-intel' > requirements.txt
```

This ensures clean, cross-platform, Docker-friendly dependencies.

---

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

## License

This project is licensed under the GPL-3.0 license.