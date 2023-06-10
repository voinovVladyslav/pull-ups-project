# Pull Ups Project

## Local setup

-   copy `.env` file

```bash
cp .env.example .env
```

-   run docker compose

```bash
docker compose up
```

-   server will be automatically up

### Optional Steps

-   create superuser

```bash
# inside python docker container
python manage.py createsuperuser
```

-   add your dependencies

```bash
# inside python docker container
pip install <package-name>
# add newly installed package to requirements
pip freeze > requirements.txt
```

-   rebuild container

```bash
docker compose build
```
