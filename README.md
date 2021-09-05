# maistodos

## Setup

The application dependencies are on `requirements.txt` and the development dependencies are on `requirements-dev.txt`.
For running the application:

```shell
> pip3 install -r requirements.txt
```

For running the application, tests and reports:

```shell
> pip3 install -r requirements-dev.txt
```

## Running the application

The default database is SQLite saving in the `storage.db` file.
Use the environment variable `DATABASE_URL` to change that.

Creating the database: `python cli.py create-database`

Running locally:

```shell
> python3 main.py
```

Use `uvicorn` to run in production:

```shell
> uvicorn main:app --log-config log.ini
```

It's also possible to use the Makefile commando for development env. Use `make runserver` for that,
this command runs with `uvicorn` and auto **reload**.

## Docs

The Swagger docs is auto generated in `<url>/docs`.

http://127.0.0.1:8000/docs

## Tests and Quality

Commands:

- Tests: `pytest`
- Lint: `flake8`
- Coverage: `coverage run -m pytest` and `coverage report -m` to create the reports.

All commands are also in the Makefile.

```shell
> make test
> make coverage
> make quality
```
