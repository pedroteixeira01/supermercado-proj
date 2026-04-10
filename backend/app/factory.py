from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up Supermercado Viva API...")
    yield
    print("Shutting down API...")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from app.api.v1.endpoints import auth, products

    app.include_router(
        products.router, prefix=f"{settings.API_V1_STR}/products", tags=["products"]
    )
    app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])

    return app
