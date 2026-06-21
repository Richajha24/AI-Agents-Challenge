from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.routes import router
from app.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize the SQLite database schemas
    await init_db()
    yield
    # Shutdown
    pass

app = FastAPI(
    title="Executive Assistant Agent API",
    description="AI-powered Executive Assistant and daily planner advisor",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)
