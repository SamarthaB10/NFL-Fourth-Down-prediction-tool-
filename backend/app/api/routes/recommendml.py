from fastapi import APIRouter
from app.schemas.RecommendSchema import RecommendMLRequest, RecommendMLResponse
from app.services.model_service import predict_coach_decision, predict_epa_options, recommend
router = APIRouter() 

@router.post("/recommended/ML", response_model=RecommendMLResponse)
def getML_Recommendation(inp: RecommendMLRequest):
    # EPA output: estimates the expected EPA for each possible fourth-down
    # action, then the recommendation below chooses the highest EPA.
    predictedepa = predict_epa_options(
        inp.yardline_100,
        inp.ydstogo,
        inp.qtr,
        inp.game_seconds_remaining,
        inp.score_differential,
    )

    # recommendation is the app's "optimal by EPA" answer, not necessarily what
    # a real coach historically would have done in the same situation.
    recommendation = recommend(
        inp.yardline_100,
        inp.ydstogo,
        inp.qtr,
        inp.game_seconds_remaining,
        inp.score_differential,
    )

    # coach_decision is a separate classifier signal. It predicts historical
    # coach behavior and class probabilities so the frontend can compare:
    # "EPA says go" vs. "coaches usually punt."
    coach_decision = predict_coach_decision(
        inp.yardline_100,
        inp.ydstogo,
        inp.qtr,
        inp.game_seconds_remaining,
        inp.score_differential,
    )
    return {
        "recommendation": recommendation,
        "predicted_epa": predictedepa,
        "Historical_coach_decision": coach_decision,
        "input": inp,
    }
