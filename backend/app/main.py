import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import analyze, report
from .engine.embeddings import warm_up


@asynccontextmanager
async def lifespan(app):
    warm_up()
    yield


app = FastAPI(title="Text Forensics", version="0.4", lifespan=lifespan)

_origins = os.environ.get("AEGIS_CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in _origins],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router, tags=["analysis"])
app.include_router(report.router, tags=["report"])


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok", "version": "0.4"}
