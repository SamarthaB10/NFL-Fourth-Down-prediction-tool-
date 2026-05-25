from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.plays import router as plays_router
from app.api.routes.summary import router as summary_router
from app.api.routes.recommend import router as recommend_router
from app.api.routes.recommendml import router as ml_router
app = FastAPI()

app.include_router(health_router)
app.include_router(plays_router)
app.include_router(summary_router)
app.include_router(recommend_router)
app.include_router(ml_router)


