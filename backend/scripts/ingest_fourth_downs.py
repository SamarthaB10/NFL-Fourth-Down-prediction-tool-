import nflreadpy
import pandas as pd
from app.services.data_cleaning import clean_fourth_down_plays
from app.models.fourth_down_play import FourthDownPlay
from app.database import SessionLocal
from typing import Optional 



def ingestPlays(season):
    db = SessionLocal() 
    try:
        pdp = nflreadpy.load_pbp(seasons=season).to_pandas()
        final_plays = clean_fourth_down_plays(pdp)
        objects = [] 

        for _,row in final_plays.iterrows(): 
            play_season = row["season"]
            week = row["week"]
            game_id = row["game_id"]
            game_date = row["game_date"]
            posteam = row["posteam"]
            defteam = row["defteam"]
            down = row["down"]
            ydstogo = row["ydstogo"]
            yardline_100 = row["yardline_100"]
            qtr = row["qtr"]
            game_seconds_remaining = row["game_seconds_remaining"]
            score_differential = row["score_differential"]
            play_type = row["play_type"]
            decision = row["decision"]
            yards_gained = row["yards_gained"]
            epa = row["epa"]
            wp = row["wp"]
            wpa = row["wpa"]
            desc = row["desc"]  
            
            play_object = FourthDownPlay(
                season = play_season,
                week = week,
                game_id = game_id,
                game_date = game_date,
                posteam = posteam,
                defteam = defteam,
                down = down,
                ydstogo = ydstogo,
                yardline_100 = yardline_100,qtr = qtr,
                game_seconds_remaining =game_seconds_remaining, 
                score_differential = score_differential,
                play_type = play_type,decision = decision, 
                yards_gained = yards_gained,
                epa = epa,wp =wp,wpa = wpa, desc =desc)
            objects.append(play_object)
        
        deleted_count = db.query(FourthDownPlay).filter(FourthDownPlay.season == season).delete()
        db.add_all(objects)
        print(f"Inserted {len(objects)} fourth-down plays for {season}.")
        print(f"Inserted {len(objects)} fourth-down plays for {season}.")
        db.flush() 
        db.commit() 
    except: 
        db.rollback() 
        raise 
    finally:
        db.close()


#one time usage to fully load in db
''' 
def FORCE_SYNC_DB(start_season = 2000, end_season =2025): 
    for season in range(start_season,end_season + 1): 
        print(f"Ingesting seaso: {season}")
        ingestPlays(season)
    print(f"Finished syncing seasons {start_season}-{end_season}.")


def sync_toModern(season): 
    ingestPlays(season)
    
    
if __name__ == "__main__": 
    FORCE_SYNC_DB(2000,2025)
'''