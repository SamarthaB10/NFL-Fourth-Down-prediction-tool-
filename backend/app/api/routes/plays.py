from fastapi import APIRouter
from app.database import SessionLocal
from app.models.fourth_down_play import FourthDownPlay



router = APIRouter() 

@router.get("/plays")
def get_plays(): 
    db = SessionLocal() 
    try:
        plays = db.query(FourthDownPlay).limit(50).all()
        results = [] 
    
        for play in plays:
            results.append({
                "season": play.season,
                "week": play.week,
                "posteam": play.posteam,
                "defteam": play.defteam,
                "decision": play.decision,
                "play_type": play.play_type,
                "ydstogo": play.ydstogo,
                "yardline_100": play.yardline_100,
                "epa": play.epa,
                "desc": play.desc,
            })
        return results
    finally: 
        db.close() 
        
        