import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .config import settings
from .database import engine, Base, SessionLocal
from .data.seed_data import seed_database

# Routers
from .routers.auth_router import router as auth_router
from .routers.game_router import router as game_router
from .routers.srs_router import router as srs_router
from .routers.editor_router import router as editor_router
from .routers.leaderboard_router import router as leaderboard_router
from .routers.cambridge_router import router as cambridge_router

# Create DB Tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(
    title="WordRhythm: 2D Rhythm Boss Battle with Spaced Repetition",
    description="A gamified rhythm language learning platform combining beat-synced boss battles with SuperMemo SM-2 spaced repetition.",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Seed database on startup
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

# Include Routers
app.include_router(auth_router)
app.include_router(game_router)
app.include_router(srs_router)
app.include_router(editor_router)
app.include_router(leaderboard_router)
app.include_router(cambridge_router)

# Health endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": "1.0.0"
    }

# Frontend path
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))

if os.path.exists(frontend_dir):
    # Mount static assets
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

    # Serve index.html
    @app.get("/")
    def serve_frontend_root():
        index_file = os.path.join(frontend_dir, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return {"message": "WordRhythm backend is running. Frontend index.html not yet built."}
