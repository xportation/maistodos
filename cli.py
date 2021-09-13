import logging

import typer

from cashback import database, models, config


logger = logging.getLogger(__name__)
db = database.Database(config.database_url(), logger)
app = typer.Typer()


@app.command('create-database')
def create_database():
    db.create_database(models.Base.metadata)


@app.callback()
def callback():
    pass


if __name__ == "__main__":
    app()
