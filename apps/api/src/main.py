from .core.config import settings
from fastapi import FastAPI
from .api.routers import claims, combos, engine_bay, health, integrity, markets, media, recommendations

app = FastAPI(title=f"{settings.app_vertical.title()} Copilot API")
app.include_router(health.router)
app.include_router(markets.router, prefix="/markets", tags=["markets"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
app.include_router(combos.router, prefix="/combos", tags=["combos"])
app.include_router(media.router, prefix="/media", tags=["media"])
app.include_router(claims.router, prefix="/claims", tags=["claims"])
app.include_router(integrity.router, prefix="/integrity", tags=["integrity"])
app.include_router(engine_bay.router, prefix="/engine-bay", tags=["engine-bay"])
