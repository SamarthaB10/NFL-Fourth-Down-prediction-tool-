import argparse
from app.services.data_cleaning import clean_fourth_down_plays
from app.models.fourth_down_play import FourthDownPlay
from app.database import SessionLocal
from app.services.pbp_cache import load_pbp_from_cache



def ingestPlays(season, *, allow_fetch=False, refresh_cache=False):
    db = SessionLocal() 
    try:
        pdp = load_pbp_from_cache(
            season,
            allow_fetch=allow_fetch,
            refresh=refresh_cache,
        )
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
        print(f"Deleted {deleted_count} existing fourth-down plays for {season}.")
        print(f"Inserted {len(objects)} fourth-down plays for {season}.")
        db.flush() 
        db.commit() 
    except: 
        db.rollback() 
        raise 
    finally:
        db.close()


def FORCE_SYNC_DB(start_season=2000, end_season=2025, *, allow_fetch=False, refresh_cache=False):
    for season in range(start_season, end_season + 1):
        print(f"Ingesting season: {season}")
        ingestPlays(season, allow_fetch=allow_fetch, refresh_cache=refresh_cache)
    print(f"Finished syncing seasons {start_season}-{end_season}.")


def sync_toModern(season, *, allow_fetch=False, refresh_cache=False):
    ingestPlays(season, allow_fetch=allow_fetch, refresh_cache=refresh_cache)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest cached NFL fourth-down play data.")
    parser.add_argument("--start-season", type=int, required=True)
    parser.add_argument("--end-season", type=int)
    parser.add_argument(
        "--fetch",
        action="store_true",
        help="Fetch missing PBP data from nflreadpy and write it to the local cache.",
    )
    parser.add_argument(
        "--refresh-cache",
        action="store_true",
        help="Re-fetch and replace cached PBP data. Requires --fetch.",
    )
    args = parser.parse_args()

    if args.refresh_cache and not args.fetch:
        parser.error("--refresh-cache requires --fetch")

    end_season = args.end_season or args.start_season
    FORCE_SYNC_DB(
        args.start_season,
        end_season,
        allow_fetch=args.fetch,
        refresh_cache=args.refresh_cache,
    )
