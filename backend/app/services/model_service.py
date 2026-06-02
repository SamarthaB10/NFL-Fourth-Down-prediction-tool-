from pathlib import Path
import joblib
import pandas as pd

# Resolve the absolute path to your models folder
MODELS_DIR = Path(__file__).resolve().parents[2] / "models"

# Load your highly optimized XGBoost models
go_model = joblib.load(MODELS_DIR / "go_epa_model.joblib")
punt_model = joblib.load(MODELS_DIR / "punt_epa_model.joblib")
fg_model = joblib.load(MODELS_DIR / "field_goal_epa_model.joblib")


def predict_epa_options(
    yardline_100: int, 
    ydstogo: int, 
    qtr: int, 
    game_seconds_remaining: int, 
    score_differential: int
):
    # Features must perfectly match the columns used in train_epa_models.py
    features = pd.DataFrame([
        {
            "yardline_100": yardline_100,
            "ydstogo": ydstogo,
            "qtr": qtr,
            "game_seconds_remaining": game_seconds_remaining,
            "score_differential": score_differential
        }
    ])
    
    # Run inferences through the XGBoost model pipelines
    go_epa = go_model.predict(features)[0]
    punt_epa = punt_model.predict(features)[0]
    field_goal_epa = fg_model.predict(features)[0]
    
    return {
        "go": round(float(go_epa), 2),
        "punt": round(float(punt_epa), 2),
        "field_goal": round(float(field_goal_epa), 2),
    }


def recommend(
    yardline_100: int, 
    ydstogo: int, 
    qtr: int, 
    game_seconds_remaining: int, 
    score_differential: int
): 
    # Forward all state metrics to the prediction function
    res = predict_epa_options(
        yardline_100, ydstogo, qtr, game_seconds_remaining, score_differential
    )
    return max(res, key=res.get)


if __name__ == "__main__": 
    # Mock situation setup (e.g., 4th & 3, trailing by 3 points in the 3rd quarter)
    yardline_test = 10
    ydstogo_test = 15
    qtr_test = 4
    seconds_rem_test = 1200
    score_diff_test = 0

    # Generate predictions using complete feature parameters
    predictions = predict_epa_options(
        yardline_test, ydstogo_test, qtr_test, seconds_rem_test, score_diff_test
    )
    print("EPA predictions:", predictions)
    
    best_option = recommend(
        yardline_test, ydstogo_test, qtr_test, seconds_rem_test, score_diff_test
    )
    
    if best_option == "field_goal": 
        print("Based on prediction, the model recommends you to kick a field goal")
    elif best_option == "go": 
        print("Based on prediction, the model recommends you to go for it")
    else:
        print("Based on prediction, the model recommends you to punt")   