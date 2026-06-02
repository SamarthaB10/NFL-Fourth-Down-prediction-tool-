from typing import Literal

from pydantic import BaseModel, Field


class SimulateRequest(BaseModel):
    yardline_100: int = Field(..., ge=1, le=99)
    ydstogo: int = Field(..., ge=1, le=30)
    qtr: int = Field(4, ge=1, le=5)
    game_seconds_remaining: int = Field(900, ge=0, le=3600)
    score_off: int = Field(0, ge=0, le=100)
    score_def: int = Field(0, ge=0, le=100)
    decision: Literal["go", "punt", "field_goal"]
    trials: int = Field(100, ge=1, le=5000)
    seed: int = Field(42, ge=0)


class PlayEventResponse(BaseModel):
    down: int
    action: str
    outcome: str
    yards_gained: int
    yardline_100: int
    points: int


class SimulateResponse(BaseModel):
    engine: str
    trials: int
    decision: str
    mean_points_scored: float
    touchdown_rate: float
    field_goal_rate: float
    punt_rate: float
    turnover_rate: float
    sample_final_score_off: int
    sample_final_score_def: int
    sample_points_scored: int
    sample_plays: list[PlayEventResponse]
