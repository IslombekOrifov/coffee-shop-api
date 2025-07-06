from fastapi import FastAPI

from app.config.settings import settings
from app.routers import auth, users

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    debug=settings.DEBUG,
)

app.include_router(auth.router)
app.include_router(users.router)