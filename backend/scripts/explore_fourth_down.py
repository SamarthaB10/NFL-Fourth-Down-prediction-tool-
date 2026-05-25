import nflreadpy as nfl
from app.services.data_cleaning import clean_fourth_down_plays
season = 2025

pbp = nfl.load_pbp(season).to_pandas()

clean_plays = clean_fourth_down_plays(pbp)

punt_epa = round(clean_plays[clean_plays["decision"] == "punt"]["epa"].mean(),2)
go_epa = round(clean_plays[clean_plays["decision"] == "go"]["epa"].mean(),2)
field_goal_epa = round(clean_plays[clean_plays["decision"] == "field_goal"]["epa"].mean(),2)
print("Season: ",season)
print("Statistics\n") 
print("Punt: count",(clean_plays["decision"] == "punt").sum(),"Average epa: ",punt_epa)
print("Go: count",(clean_plays["decision"] == "go").sum(),"Average epa: ",go_epa)
print("Field_goal: count",(clean_plays["decision"] == "field_goal").sum(),"Average epa:",field_goal_epa)
