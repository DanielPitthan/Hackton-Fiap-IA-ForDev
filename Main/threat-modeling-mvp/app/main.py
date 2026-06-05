"""
Threat Modeling MVP — FastAPI Application Entry Point
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import analysis, reports, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown events."""
    # Startup
    print(f"[{settings.APP_NAME}] Starting up in '{settings.APP_ENV}' mode…")
    yield
    # Shutdown
    print(f"[{settings.APP_NAME}] Shutting down.")


app = FastAPI(
    title="Threat Modeling MVP",
    description=(
        "Recebe imagens de diagramas de arquitetura e gera automaticamente "
        "relatórios de Modelagem de Ameaças usando a metodologia STRIDE."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

# ─── CORS ────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ─────────────────────────────────────────────────────────────────
app.include_router(health.router, tags=["Health"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["Analysis"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports"])


@app.get("/", tags=["Root"])
async def root():
    return {
        "service": "Threat Modeling MVP",
        "version": "0.1.0",
        "docs": "/docs",
    }
