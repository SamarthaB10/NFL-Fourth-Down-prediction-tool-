# NFL 4D

NFL 4D is a full-stack fourth-down decision engine. It uses historical NFL play-by-play data to recommend whether an offense should go for it, punt, or kick a field goal on fourth down.

The backend ingests nflverse play-by-play data with `nflreadpy`, cleans fourth-down plays, stores them in PostgreSQL, and exposes FastAPI endpoints for summaries, historical recommendations, and ML-based EPA predictions.

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- nflreadpy / nflverse
- pandas
- scikit-learn
- joblib
