from pathlib import Path
import joblib
import pandas as pd

# Resolve the absolute path to your models folder
MODELS_DIR = Path(__file__).resolve().parents[2] / "models"

# These three models are EPA regressors. Each one predicts the expected EPA
# for one possible fourth-down choice, then recommend() picks the highest EPA.
go_model = joblib.load(MODELS_DIR / "go_epa_model.joblib")
punt_model = joblib.load(MODELS_DIR / "punt_epa_model.joblib")
fg_model = joblib.load(MODELS_DIR / "field_goal_epa_model.joblib")

# The coach classifier is intentionally separate from the EPA models.
# It answers a different question: "What would historical coaches probably do
# in this situation?" It does not decide which choice has the best EPA.
coach_model_path = MODELS_DIR / "coach_decision_model.joblib"

# Load the coach classifier only if the artifact exists. This lets the API keep
# running even before scripts/train_coach_classifier.py has been run locally.
coach_model_bundle = joblib.load(coach_model_path) if coach_model_path.exists() else None


def build_features(
    yardline_100: int,
    ydstogo: int,
    qtr: int,
    game_seconds_remaining: int,
    score_differential: int,
):
    # All ML models in this file were trained on this same game-state feature
    # set. Keeping feature construction in one helper prevents the EPA models
    # and coach classifier from accidentally receiving different columns.
    return pd.DataFrame(
        [
            {
                "yardline_100": yardline_100,
                "ydstogo": ydstogo,
                "qtr": qtr,
                "game_seconds_remaining": game_seconds_remaining,
                "score_differential": score_differential,
            }
        ]
    )


def predict_epa_options(
    yardline_100: int, 
    ydstogo: int, 
    qtr: int, 
    game_seconds_remaining: int, 
    score_differential: int
):
    # Features must perfectly match the columns used in train_epa_models.py
    features = build_features(
        yardline_100, ydstogo, qtr, game_seconds_remaining, score_differential
    )
    
    # Run the same game state through each decision-specific EPA model.
    # Important limitation: these models were trained on historical plays where
    # that decision was actually chosen, so they still carry selection bias.
    go_epa = go_model.predict(features)[0]
    punt_epa = punt_model.predict(features)[0]
    field_goal_epa = fg_model.predict(features)[0]
    
    return {
        "go": round(float(go_epa), 2),
        "punt": round(float(punt_epa), 2),
        "field_goal": round(float(field_goal_epa), 2),
    }


def predict_coach_decision(
    yardline_100: int,
    ydstogo: int,
    qtr: int,
    game_seconds_remaining: int,
    score_differential: int,
):
    # If the classifier has not been trained yet, return None instead of
    # crashing the endpoint. The response will still include the EPA output.
    if coach_model_bundle is None:
        return None

    # train_coach_classifier.py saves a bundle, not just the XGBoost model:
    # - model: the classifier
    # - label_encoder: maps numeric classes back to field_goal/go/punt
    # - feature_cols: preserves the exact training column order
    model = coach_model_bundle["model"]
    label_encoder = coach_model_bundle["label_encoder"]
    feature_cols = coach_model_bundle["feature_cols"]

    # Reorder columns using the saved training metadata. XGBoost is sensitive
    # to feature order, so this avoids subtle prediction bugs if code changes.
    features = build_features(
        yardline_100, ydstogo, qtr, game_seconds_remaining, score_differential
    )[feature_cols]

    # prediction is the most likely historical coach decision.
    # probabilities gives confidence for every class, which is useful when EPA
    # and coach behavior disagree.
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    classes = label_encoder.classes_

    return {
        "decision": str(label_encoder.inverse_transform([prediction])[0]),
        "probabilities": {
            str(decision): round(float(probability), 3)
            for decision, probability in zip(classes, probabilities)
        },
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
