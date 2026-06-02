from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.plays import router as plays_router
from app.api.routes.summary import router as summary_router
from app.api.routes.recommend import router as recommend_router
from app.api.routes.recommendML import router as ml_router
from app.api.routes.simulate import router as simulate_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="NFL 4D API")



app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(plays_router)
app.include_router(summary_router)
app.include_router(recommend_router)
app.include_router(ml_router)
app.include_router(simulate_router)


