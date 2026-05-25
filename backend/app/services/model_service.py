from pathlib import Path
import joblib
import pandas as pd

MODELS_DIR = Path(__file__).resolve().parents[2] / "models"
go_model = joblib.load(MODELS_DIR/"go_epa_model.joblib")
punt_model = joblib.load(MODELS_DIR/"punt_epa_model.joblib")
fg_model = joblib.load(MODELS_DIR/"field_goal_epa_model.joblib")



def predict_epa_options(yardline_100:int, ydstogo:int):
    features = pd.DataFrame([
    {
        "yardline_100": yardline_100,
        "ydstogo": ydstogo,
    }
    ])
    go_epa = go_model.predict(features)[0]
    punt_epa = punt_model.predict(features)[0]
    field_goal_epa = fg_model.predict(features)[0]
    return {
        "go": round(float(go_epa), 2),
        "punt": round(float(punt_epa), 2),
        "field_goal": round(float(field_goal_epa), 2),
    }


def recommend(yardline:int, ydstogo:int): 
    res = predict_epa_options(yardline,ydstogo)
    return max(res,key=res.get)

if __name__ == "__main__": 
    yardline_100 = 43
    ydstogo = 3
    print("EPA prediction", predict_epa_options(yardline_100,ydstogo))
    res = recommend(yardline_100,ydstogo)
    if res == "field_goal": 
        print("Based on prediction, the model recommends you to kick a field goal")
    elif res == "go": 
        print("Based on prediction, the model recommends you to go for it")
    else:
        print("Based on prediction, the model recommends you to punt")
        