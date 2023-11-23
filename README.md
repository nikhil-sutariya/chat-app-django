
# Django chat app

Here is a chat app with user's authentication apis with django rest framework.


## Installation
### 1. Linux

```bash
# Create python virtual environment
python3 -m venv venv

# Activate the python virtual environment
source venv/bin/activate

# Install the requirements for the project into the virtual environment
pip install -r requirements.txt
```

### 2. Windows

```bash
# Create python virtual environment
conda create --name venv python=3.8.10

# Activate the python virtual environment
conda activate venv

# Install the requirements for the project into the virtual environment
python -m pip install --upgrade pip
pip install -r requirements.txt

```

## Run Locally

### 1. Linux

```bash
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

### 2. Windows

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
