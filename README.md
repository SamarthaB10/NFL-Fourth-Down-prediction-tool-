NFL 4D is a full-stack NFL fourth-down decision engine that compares data-driven strategy against historical coaching tendencies.

  The app ingests NFL play-by-play data, cleans fourth-down situations, stores processed plays in PostgreSQL, and serves recommendations through a FastAPI backend. The frontend provides an interactive decision tool for comparing whether
  an offense should go for it, punt, or kick a field goal.

  ## What It Does

  NFL 4D supports two types of fourth-down analysis:

  1. **Historical EPA lookup**
     - Finds similar historical fourth-down situations.
     - Compares average Expected Points Added by decision.
     - Recommends the option with the strongest historical EPA.

  2. **Machine learning prediction**
     - Uses game context such as field position, yards to go, quarter, time remaining, and score differential.
     - Runs separate EPA regression models for go, punt, and field-goal decisions.
     - Adds a historical coach classifier that predicts what coaches would likely choose in the same situation.

  This creates a useful comparison:

  ```text
  EPA model: What has the highest expected value?
  Coach classifier: What would coaches historically do?

  ## Tech Stack

  ### Backend

  - Python
  - FastAPI
  - PostgreSQL
  - SQLAlchemy
  - Pydantic
  - pandas
  - nflreadpy / nflverse
  - XGBoost
  - scikit-learn
  - joblib

  ### Frontend

  - React
  - Vite
  - JavaScript
  - CSS

  ## Project Structure

  backend/
    app/
      api/routes/
        health.py
        plays.py
        recommend.py
        recommendml.py
        summary.py
      models/
        fourth_down_play.py
      schemas/
        RecommendSchema.py
      services/
        data_cleaning.py
        model_service.py
        pbp_cache.py
    models/
      go_epa_model.joblib
      punt_epa_model.joblib
      field_goal_epa_model.joblib
      coach_decision_model.joblib
    scripts/
      create_tables.py
      ingest_fourth_downs.py
      train_epa_models.py
      train_coach_classifier.py

  frontend/
    src/
      api/
      components/
      pages/
      utils/

  ## Setup

  ### 1. Backend

  cd backend
  pip install -r requirements-core.txt

  Create a .env file in backend/:

  DATABASE_URL=postgresql+psycopg://USER:PASSWORD@localhost:5432/DB_NAME

  Create database tables:

  python scripts/create_tables.py

  Ingest fourth-down data:

  PYTHONPATH=. python scripts/ingest_fourth_downs.py

  Train EPA models:

  PYTHONPATH=. python scripts/train_epa_models.py

  Train coach classifier:

  PYTHONPATH=. python scripts/train_coach_classifier.py

  Run the API:

  python3 -m uvicorn app.main:app --reload

  API docs:

  http://127.0.0.1:8000/docs

  ### 2. Frontend

  cd frontend
  npm install
  npm run dev

  Frontend app:

  http://localhost:5173

  ## API Overview

   Endpoint                 Description
  ━━━━━━━━━━━━━━━━━━━━━━━  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   GET /health              API health check
  ───────────────────────  ────────────────────────────────────────────────────
   GET /plays               Returns stored fourth-down plays
  ───────────────────────  ────────────────────────────────────────────────────
   GET /summary/{season}    Returns season-level fourth-down summary
  ───────────────────────  ────────────────────────────────────────────────────
   POST /recommend          Historical EPA recommendation
  ───────────────────────  ────────────────────────────────────────────────────
   POST /recommended/ML     ML EPA prediction plus historical coach classifier

  ## Example ML Request

  curl -X POST http://127.0.0.1:8000/recommended/ML \
    -H "Content-Type: application/json" \
    -d '{
      "yardline_100": 45,
      "ydstogo": 4,
      "qtr": 4,
      "game_seconds_remaining": 900,
      "score_differential": 0
    }'

  Example response:

  {
    "recommendation": "go",
    "predicted_epa": {
      "go": 0.4,
      "punt": -0.32,
      "field_goal": -0.77
    },
    "Historical_coach_decision": {
      "decision": "punt",
      "probabilities": {
        "field_goal": 0.002,
        "go": 0.078,
        "punt": 0.92
      }
    }
  }

  ## Machine Learning Approach

  NFL 4D uses two different ML approaches:

  ### EPA Regression Models

  The EPA models estimate Expected Points Added for each possible fourth-down decision.

  Separate regression models are trained for:

  go
  punt
  field_goal

  Each model predicts the expected EPA for that decision given the game context.

  ### Historical Coach Classifier

  The coach classifier is a multiclass classification model. It predicts what historical coaches would most likely choose:

  go
  punt
  field_goal

  This allows the app to compare analytically optimal decisions against real-world coaching tendencies.

  ## Future Improvements

  - Improve counterfactual modeling for alternative fourth-down choices.
  - Optimize PostgreSQL queries for faster historical lookups.
  - Add richer model evaluation dashboards.
  - Expand feature engineering with team strength, weather, and win probability context.
.
