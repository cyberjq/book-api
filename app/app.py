from fastapi import FastAPI

from app.api.routers import (
    author,
    book,
    publishing_house,
    subject,
    warehouse
)
from config import config


def create_app() -> FastAPI:
    app = FastAPI(debug=config.APP_CONFIG.debug)
    app.include_router(author.router)
    app.include_router(book.router)
    app.include_router(publishing_house.router)
    app.include_router(subject.router)
    app.include_router(warehouse.router)

    return app


app = create_app()


@app.on_event("startup")
async def startup_event():
    ...