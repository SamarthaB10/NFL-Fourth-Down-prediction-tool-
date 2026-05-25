from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
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
            "decision": play.decision, 
            "yardline_100": play.yardline_100,
            "ydstogo": play.ydstogo,
            "epa": play.epa
        })
finally: 
    db.close()

df = pd.DataFrame(rows)
df = df.dropna(subset=["decision", "yardline_100", "ydstogo", "epa"])

models_dir = Path("models")
models_dir.mkdir(exist_ok=True)


feature_cols = ["yardline_100", "ydstogo"]

for decision in ["go", "punt", "field_goal"]:
    decision_df = df[df["decision"] == decision]
    X = decision_df[feature_cols]
    y = decision_df["epa"]
    X_train, X_test, y_train, y_test = train_test_split( X, y,test_size=0.2,random_state=42,)
    model = RandomForestRegressor(n_estimators= 300,random_state=42)
    model.fit(X_train,y_train)
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    print(f"{decision} MAE: {round(mae, 3)}")
    model_path = models_dir / f"{decision}_epa_model.joblib"
    joblib.dump(model, model_path)
    print(f"Saved {model_path}")