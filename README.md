# KnigaPoisk

## Description

Оnline book service written in Django Framework.

## Installation

[Install `Docker Compose`](https://docs.docker.com/compose/install/).

## Run

```bash
docker compose build
docker compose run --rm django python3 manage.py makemigrations
docker compose run --rm django python3 manage.py migrate
docker compose run --rm django python3 manage.py createsuperuser
docker compose up
```

## License

[MIT](LICENSE)
