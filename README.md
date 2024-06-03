# django-tiniest

A template for a Django project in one file.


## Setting up virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


## Running the application

### Development server:

```bash
python app.py runserver 8000
```

### Gunicorn:
```bash
gunicorn app
```

### Uvicorn:
```bash
uvicorn app:application
```

**Note:** You need to change one line in `app.py`. Search for `"ASGI"` in `app.py`.
