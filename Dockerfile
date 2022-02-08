ARG PYTHON_VERSION=3.10-alpine

# define an alias for the specfic python version used in this file.
FROM python:${PYTHON_VERSION} as python

# Python build stage
FROM python as python-build-stage

WORKDIR /app

# Install apt packages
RUN apk update --no-cache \
# dependencies for building Python packages
&& apk add build-base libffi-dev musl-dev openssl-dev cargo postgresql-dev libpq curl curl-dev git --no-cache --virtual .build-deps \
# upgrade pip to the newest version
&& pip install --no-cache-dir --upgrade pip

# install poetry
RUN curl -sSL https://install.python-poetry.org | python3 - 

# copy poetry project and lock file
COPY pyproject.toml .
COPY poetry.lock .
# Requirements are installed here to ensure they will be cached.
RUN /root/.local/bin/poetry export --without-hashes > requirements.txt 

# Create Python Dependency and Sub-Dependency Wheels.
RUN pip wheel --wheel-dir /usr/src/app/wheels  \
  -r requirements.txt

# Python 'run' stage
FROM python as python-run-stage

ARG APP_HOME=/app

RUN addgroup --system django \
    && adduser --system --ingroup django django

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR ${APP_HOME}

# Install required system dependencies
RUN apk update \
    && apk add postgresql-libs libpq gettext curl --no-cache \
    && rm -rf /var/cache/apk/*

# All absolute dir copies ignore workdir instruction. All relative dir copies are wrt to the workdir instruction
# copy python dependency wheels from python-build-stage
COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

# use wheels to install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
	&& rm -rf /wheels/

COPY --chown=django:django ./bin/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY --chown=django:django ./bin/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# copy application code to WORKDIR
COPY  --chown=django:django . ${APP_HOME}

# make django owner of the WORKDIR directory as well.
RUN chown django:django ${APP_HOME}

USER django

ENTRYPOINT ["/entrypoint"]
