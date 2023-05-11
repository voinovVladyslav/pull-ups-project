# Pull Ups Project

## Local setup

-   copy `.env` file

```bash
cp .env.example .env
```

-   make virtual environment

```bash
python -m venv venv
```

-   install dependencies

```bash
pip install -r requirements.txt
```

-   make migrations

```bash
python manage.py migrate
```

-   run server

```bash
python manage.py runserver
```

### Optional Steps

-   create superuser

```bash
python manage.py createsuperuser
```

-   add your dependencies

```bash
# make sure virtual environment is on
pip install <package-name>
# add newly installed package to requirements
pip freeze > requirements.txt
```
