from pathlib import Path 
import joblib
import pandas as pd

from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,log_loss
from sklearn.preprocessing import LabelEncoder
from app.database import SessionLocal
from app.models.fourth_down_play import FourthDownPlay



db = SessionLocal() 

try: 
    plays = db.query(FourthDownPlay).all()
    
    rows = [] 
    for play in plays: 
        rows.append({
            "decision" : play.decision, 
            "yardline_100": play.yardline_100,
            "ydstogo": play.ydstogo, 
            "qtr" : play.qtr, 
            "game_seconds_remaining" : play.game_seconds_remaining, 
            "score_differential" : play.score_differential
        })
        
finally: 
    db.close() 
    

df = pd.DataFrame(rows)


feature_cols = [
      "yardline_100",
      "ydstogo",
      "qtr",
      "game_seconds_remaining",
      "score_differential",]
target_col = "decision"
required_cols = [target_col, *feature_cols]

df = df.dropna(subset=required_cols)

X = df[feature_cols]
y = df[target_col]

label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded,
)

model = XGBClassifier(
    n_estimators=450,
    learning_rate=0.04,
    max_depth=4,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="multi:softprob",
    eval_metric="mlogloss",
    random_state=42,
    n_jobs=-1,
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)

print("Classes:", list(label_encoder.classes_))
print(classification_report(y_test, predictions, target_names=label_encoder.classes_))
print("Log loss:", round(log_loss(y_test, probabilities), 4))

models_dir = Path("models")
models_dir.mkdir(exist_ok=True)

model_path = models_dir / "coach_decision_model.joblib"
joblib.dump(
    {
        "model": model,
        "label_encoder": label_encoder,
        "feature_cols": feature_cols,
        "target_col": target_col,
    },
    model_path,
)

print(f"Saved {model_path}")
