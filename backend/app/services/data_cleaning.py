
def filter_fourth_downs(pbp): 
    fourth_downs = pbp[
    (pbp["down"] == 4)
    & (pbp["play_type"].isin(["run", "pass", "punt", "field_goal"]))].copy() 
    return fourth_downs


def add_decision_column(pbp): 
    pbp["decision"] = pbp["play_type"].replace({
        "run":"go",
        "pass":"go",
        "field_goal":"field_goal",
        "punt":"punt"
    })
    return pbp

def clean_fourth_down_plays(pbp):
    fourth_downs = filter_fourth_downs(pbp) 
    clean_fourth_down_plays = add_decision_column(fourth_downs)
    return clean_fourth_down_plays