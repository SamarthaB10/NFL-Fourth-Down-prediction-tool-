from pathlib import Path

import joblib
import pandas as pd
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

from app.database import SessionLocal
from app.models.fourth_down_play import FourthDownPlay


db = SessionLocal()
try:
    plays = db.query(FourthDownPlay).all()
    rows = []
    for play in plays: 
        rows.append({
            "qtr" : play.qtr,
            "game_seconds_remaining":play.game_seconds_remaining,
            "score_differential": play.score_differential,
            "decision": play.decision, 
            "yardline_100": play.yardline_100,
            "ydstogo": play.ydstogo,
            
            "epa": play.epa
        })
finally: 
    db.close()

df = pd.DataFrame(rows)
required_cols =["decision", "yardline_100", "ydstogo", "epa", "qtr", "game_seconds_remaining", "score_differential"]

df = df.dropna(subset=required_cols)

models_dir = Path("models")
models_dir.mkdir(exist_ok=True)


feature_cols = ["yardline_100", "ydstogo", "qtr", "game_seconds_remaining", "score_differential"]

for decision in ["go", "punt", "field_goal"]:
    decision_df = df[df["decision"] == decision]
    if len(decision_df) < 50: 
        continue 
    
    X = decision_df[feature_cols]
    y = decision_df["epa"]
    X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2,random_state=42,)
    model = XGBRegressor(
        n_estimators=400,
        learning_rate=0.03,    # Lower learning rate avoids overfitting noise
        max_depth=5,           # Limits deep tracking splits 
        subsample=0.8,         # Row data regularizer fraction
        colsample_bytree=0.8,  # Column tracking selection parameter fraction
        random_state=42,
        n_jobs=-1              # Utilize all available CPU threads
    )
    model.fit(X_train,y_train)
    
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    print(f"{decision} MAE: {round(mae, 3)}")
    model_path = models_dir / f"{decision}_epa_model.joblib"
    joblib.dump(model, model_path)
    print(f"Saved {model_path}")