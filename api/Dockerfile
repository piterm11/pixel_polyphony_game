FROM python:3.9-buster as base


ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_VIRTUALENVS_CREATE=true \
    POETRY_NO_INTERACTION=1

ENV PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


FROM base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

WORKDIR $PYSETUP_PATH
COPY pyproject.toml ./
RUN poetry install --no-dev

# development version
FROM base as development

ENV RUN_ENV=development

WORKDIR $PYSETUP_PATH
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
RUN poetry install

WORKDIR /app/
EXPOSE 8000
CMD ["sh", "-c", "daphne --bind 0.0.0.0 core.asgi:application && python manage.py runworker -v2"]



# production version
FROM base as production

ENV RUN_ENV=production

COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY . /app/
WORKDIR /app
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0", "-k", "uvicorn.workers.UvicornWorker", "core.asgi:application"]
