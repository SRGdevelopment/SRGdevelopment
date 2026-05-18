from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routers import claims, combos, health, integrity, markets, media, recommendations
from .core.config import settings

app = FastAPI(title="Sports Bet Copilot API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(health.router)
app.include_router(markets.router, prefix="/markets", tags=["markets"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
app.include_router(combos.router, prefix="/combos", tags=["combos"])
app.include_router(media.router, prefix="/media", tags=["media"])
app.include_router(claims.router, prefix="/claims", tags=["claims"])

app.include_router(integrity.router, prefix="/integrity", tags=["integrity"])
