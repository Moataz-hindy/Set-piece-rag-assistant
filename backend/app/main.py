from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import query
from app.core.config import settings
from app.services.retrieval import retrieval_service
from contextlib import asynccontextmanager
import logging

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load the vector store
    try:
        retrieval_service.initialize()
    except Exception as e:
        logging.error(f"Failed to load vector store: {e}")
        # Note: If Chroma DB isn't built yet, this will fail gracefully.
    yield
    # Shutdown

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query.router)
