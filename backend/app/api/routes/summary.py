from fastapi import APIRouter

from app.database import SessionLocal
from app.models.fourth_down_play import FourthDownPlay


router = APIRouter()


@router.get("/summary/{season}")
def get_summary(season: int):
    db = SessionLocal()

    try:
        plays = db.query(FourthDownPlay).filter(
            FourthDownPlay.season == season
        ).all()
        

        if not plays:
            return {
                "season": season,
                "total_plays": 0,
                "message": "No plays found. Run ingestion first.",
            }

        decision_counts = {}
        epa_totals = {}

        for play in plays:
            decision_counts[play.decision] = decision_counts.get(play.decision, 0) + 1
            epa_totals[play.decision] = epa_totals.get(play.decision, 0) + play.epa
        
        usable_play_count = sum(decision_counts.values())
        average_epa = {}

        for decision in decision_counts:
            average_epa[decision] = round(
                epa_totals[decision] / decision_counts[decision],
                2,
            )

        return {
            "season": season,
            "usable_plays": usable_play_count,
            "decision_counts": decision_counts,
            "average_epa": average_epa,
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        db.close()