import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers import api, twilio
from app.utils.logger import get_logger
from database import STORAGE_BASE, init_db

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Twilio POC backend")
    init_db()
    logger.info("Database initialized and seeded")
    yield
    logger.info("Shutting down Twilio POC backend")


app = FastAPI(
    title="Twilio POC",
    description="Proof of concept for Twilio communication with FastAPI",
    version="0.2.0",
    lifespan=lifespan,
)

cors_origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]
_frontend_url = os.getenv("FRONTEND_URL", "")
if _frontend_url:
    cors_origins.append(_frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(twilio.router)
app.include_router(api.router)
app.mount("/storage", StaticFiles(directory=str(STORAGE_BASE)), name="storage")
