from fastapi import FastAPI

from cashback import views


def create_app():
    app = FastAPI()
    app.include_router(views.router)
    return app
