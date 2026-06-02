from fastapi import APIRouter
from app.schemas.RecommendSchema import RecommendMLRequest, RecommendMLResponse
from app.services.model_service import predict_epa_options, recommend
router = APIRouter() 

@router.post("/recommended/ML", response_model=RecommendMLResponse)
def getML_Recommendation(inp: RecommendMLRequest):
    predictedepa = predict_epa_options(
        inp.yardline_100,
        inp.ydstogo,
        inp.qtr,
        inp.game_seconds_remaining,
        inp.score_differential,
    )
    recommendation = recommend(
        inp.yardline_100,
        inp.ydstogo,
        inp.qtr,
        inp.game_seconds_remaining,
        inp.score_differential,
    )
    return {
        "recommendation": recommendation,
        "predicted_epa": predictedepa,
        "input": inp,
    }