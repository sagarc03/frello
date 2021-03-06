# Frello

An issue tracker / project management tool created for the semeter long assignment for CIS 594 Software Testing Principal & Techniques.

### Features

#### VERSION 1

- Login: Ability for users to sign into the application.
- Account Creation: Ability for potential users to create an account.
- Contributors Add: Add contributor to a project
- Issue/Task Creation: Ability to create task/issue specifying the task details and status.

#### VERSION 2

- TBD

# Learning Objectives

- Perfom complete system test (every new release)
- Keep track of risk for the project
- Maintian project using a VCS.

# Development

Its recomended to set up docker, and use docker-compose workflow suggests below for your developement process. It is the fastest way to set up.

## Using docker compose

Docker Compose relies on Docker Engine for any meaningful work, so make sure you have Docker Engine installed either locally or remote, depending on your setup. You can read about setup [here](https://docs.docker.com/compose/install/).

When using docker compose for local developement you don't need to have postgres server or mailhog locally running. Docker compose will set up and run all these services and make them available for django to use. The repo comes pre-configured for this set up so you don't need change/add any extra config.

Everytime you add a new dependencies to the application or want to rebuild the image before you run the application using,

```bash
docker-compose up --build

# run without building
docker-compose up
```

After change in the application data model you would want to generate migrations, this can be done using. Make sure you have docker-compose running in another shell or in background before you run any command.

```bash
# Note: you need to have docker-compose running using `docker-compose up` before you can run this.

docker-compose exec app poetry run python manage.py makemigration <app_name>
docker-compose exec app poetry run python manage.py migrate
```

This project uses pytest as its test runner, you can run tests,

```bash
# Note: you need to have docker-compose running using `docker-compose up` before you can run this.

docker-compose exec app poetry run pytest
```

Runing <x> command,

```bash
# Note: you need to have docker-compose running using `docker-compose up` before you can run this.

docker-compose exec app  <x>
```

# Contributors

- [@sagarc03](https://github.com/sagarc03)

## Local

The project is manged using [poetry](https://python-poetry.org/). Instruction to install and setup poetry can be found [here](https://python-poetry.org/docs/master/#installation). The application also uses [postgres](https://www.postgresql.org/) as its primary database and [mailhog](https://github.com/mailhog/MailHog) as email client during developement. You can manage the config from the `config` module.

Once all the dependencies are resolved, you can start the server using,

```bash
# without activating the virtual environment
poetry run python manage.py runserver

# With active virtial environment
python manage.py runserver
```

Running migrations

```bash
# without activating the virtual environment
poetry run python manage.py makemigration <app_name>
poetry run python manage.py migrate

# With active virtial environment
python manage.py makemigration <app_name>
python manage.py migrate
```

You can run tests using,

```bash
# without activating the virtual environment
poetry run pytest

# With active virtial environment
pytest
```

check
