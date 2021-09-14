from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from sqlalchemy.exc import IntegrityError

from cashback import views, di


def register_exceptions(app):
    @app.exception_handler(IntegrityError)
    async def database_integrity_error(_, e):
        return PlainTextResponse(str(e), status_code=400)


def create_app():
    container = di.Container()
    container.wire(modules=[views])

    app = FastAPI()
    register_exceptions(app)
    app.container = container
    app.include_router(views.router)
    return app
