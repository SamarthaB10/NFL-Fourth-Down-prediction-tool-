from fastapi import APIRouter

from app.schemas.simulate_schema import PlayEventResponse, SimulateRequest, SimulateResponse
from app.services.possession_simulator import run_monte_carlo

router = APIRouter(prefix="/simulate", tags=["simulate"])


@router.post("/possession", response_model=SimulateResponse)
def simulate_possession(body: SimulateRequest):
    stats = run_monte_carlo(
        yardline_100=body.yardline_100,
        ydstogo=body.ydstogo,
        decision=body.decision,
        trials=body.trials,
        qtr=body.qtr,
        game_seconds_remaining=body.game_seconds_remaining,
        score_off=body.score_off,
        score_def=body.score_def,
        seed=body.seed,
    )
    sample = stats["sample"]
    return SimulateResponse(
        engine=stats["engine"],
        trials=stats["trials"],
        decision=body.decision,
        mean_points_scored=stats["mean_points_scored"],
        touchdown_rate=stats["touchdown_rate"],
        field_goal_rate=stats["field_goal_rate"],
        punt_rate=stats["punt_rate"],
        turnover_rate=stats["turnover_rate"],
        sample_final_score_off=sample.final_score_off,
        sample_final_score_def=sample.final_score_def,
        sample_points_scored=sample.points_scored,
        sample_plays=[
            PlayEventResponse(
                down=p.down,
                action=p.action,
                outcome=p.outcome,
                yards_gained=p.yards_gained,
                yardline_100=p.yardline_100,
                points=p.points,
            )
            for p in sample.plays
        ],
    )
