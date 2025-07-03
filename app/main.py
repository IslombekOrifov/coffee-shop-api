from fastapi import FastAPI

from app.config.settings import settings


def create_app():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        debug=settings.DEBUG,
    )

    return app

app = create_app()