# **Pixel Polyphony Game**

## How to use

1. Get repo
2. Create environment variables file in main directory typing command: `touch .env`
3. Populate .env according to the *Environment Variables Setup* section.
3. Think before modify
4. Modify
5. Think before use
6. Use
7. Enjoy the time saved

## Running development stack

``` sh
docker-compose -f docker-compose.yaml -f docker-compose.dev.yaml up --build
```

## Running "production" stack

``` sh
docker-compose -f docker-compose.yaml up --build
```

## Environment Variables Setup:

Environment variables file (.env) should be created as described below:  

`Postgres`  
POSTGRES_DB=POSTGRES DATABASE NAME  
POSTGRES_USER=POSTGRES DATABASE USER  
POSTGRES_PASSWORD=POSTGRES DATABASE PASSWORD  
POSTGRES_HOST=DATABASE SERVICE HOSTNAME (default db) # Optional  
POSTGRES_PORT=DATABASE PORT NUMBER (default 5432) # Optional  

`Django`  
SECRET_KEY=DJANGO SECRET KEY  
DEBUG=DEBUG MODE (default False) # Optional  
ALLOWED_HOSTS=LIST OF ALLOWED HOSTS   
DJANGO_LOG_LEVEL=DJANGO LOG LEVEL (default WARNING) # Optional

`Celery`  
CELERY_BROKER_URL=CELERY BROKER URL  
CELERY_RESULT_BACKEND=CELERY RESULT BACKEND  

`Media`  
MEDIA_URL=MEDIA CONTENT BASE URL  
STATIC_URL=STATIC CONTENT BASE URL  

## Features

- `multi-stage` docker images
- `Docker Compose` with multiple compose files
- Monorepo-friendly structure
- `Poetry` for `Python 3.9`
- Prod stack: `Gunicorn` + `UvicornWorker`
- Dev stack: `Uvicorn` with shared code directory and autoreload
  
## Useful documentation

- Docker: <https://docs.docker.com/>
- Docker Compose: <https://docs.docker.com/compose/>
- Git-flow: <https://git-flow.readthedocs.io/en/latest/index.html>
- Poetry: <https://python-poetry.org/docs/>
- Uvicorn: <https://www.uvicorn.org/>
- Gunicorn: <https://docs.gunicorn.org/en/stable/index.html>
