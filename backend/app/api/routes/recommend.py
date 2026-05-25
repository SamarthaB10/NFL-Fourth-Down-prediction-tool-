from fastapi import APIRouter
from app.schemas.RecommendSchema import RecommendationRequest,RecommendationResponse
from app.database import SessionLocal
from app.models.fourth_down_play import FourthDownPlay

router = APIRouter()


@router.post("/recommend",response_model=RecommendationResponse)
def app_recommend(inp: RecommendationRequest) -> RecommendationResponse: 
    yardLine_100= inp.yardline_100
    yds_togo = inp.ydstogo
    season = inp.season
    db = SessionLocal()
    
    decision_counts ={}
    epa_totals = {}
    average_epa = {} 
    try: 
        plays_query = db.query(FourthDownPlay).filter(
            FourthDownPlay.season < season,
            FourthDownPlay.yardline_100 >=yardLine_100 -5,
            FourthDownPlay.yardline_100 <= yardLine_100 + 5, 
            FourthDownPlay.ydstogo >= yds_togo- 2, 
            FourthDownPlay.ydstogo <= yds_togo + 2,
            )
        if inp.posteam:
            plays_query = plays_query.filter(FourthDownPlay.posteam == inp.posteam)
        if inp.defteam:
            plays_query = plays_query.filter(FourthDownPlay.defteam == inp.defteam)
        plays = plays_query.all()
        for play in plays: 
            if play.epa is None: 
                continue 
            decision_counts[play.decision] = decision_counts.get(play.decision,0) + 1    
            epa_totals[play.decision] = epa_totals.get(play.decision, 0) + play.epa
        
        for decision in decision_counts:
            average_epa[decision] = round(
            epa_totals[decision] / decision_counts[decision],
            2
        )
        
        if not average_epa:
            return {
                "recommendation": None,
                "options": {
                    "go": {"count": 0, "avgEpa": None},
                    "punt": {"count": 0, "avgEpa": None},
                    "field_goal": {"count": 0, "avgEpa": None},
                },
                "historical_context": {
                    "similarPlays": 0,
                    "decisionCounts": {},
                    "averageEpa": {},
                },
                "input": inp,
                "message": "No similar historical plays found.",
            }
        recommendation = max(average_epa, key = average_epa.get)
        return {
            "recommendation": recommendation,
            "options": {
                "go": {
                    "count": decision_counts.get("go", 0),
                    "avgEpa": average_epa.get("go"),
                },
                "punt": {
                    "count": decision_counts.get("punt", 0),
                    "avgEpa": average_epa.get("punt"),
                },
                "field_goal": {
                    "count": decision_counts.get("field_goal", 0),
                    "avgEpa": average_epa.get("field_goal"),
                },
            },
            "historical_context": {
                "similarPlays": sum(decision_counts.values()),
                "decisionCounts": decision_counts,
                "averageEpa": average_epa,
            },
            "input": inp,
            "message": None,
        }
    finally:
        db.close() 