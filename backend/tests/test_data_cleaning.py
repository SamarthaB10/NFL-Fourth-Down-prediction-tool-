import pandas as pd 
from app.services.data_cleaning import clean_fourth_down_plays


fake_pbp = pd.DataFrame({
    "down": [4, 4, 4, 4, 4, 3, 1, 4],
    "play_type": [
        "run",
        "pass",
        "punt",
        "field_goal",
        "no_play",
        "pass",
        "run",
        None,
    ],
    "epa": [0.5, 1.2, -0.1, 0.3, 0.0, 0.8, 0.4, None],
})

result = clean_fourth_down_plays(fake_pbp)

goplays = result[result["decision"] == "go"]
print(goplays)