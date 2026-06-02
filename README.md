# NFL 4D

NFL 4D is a full-stack fourth-down decision engine. It uses historical NFL play-by-play data to recommend whether an offense should go for it, punt, or kick a field goal on fourth down.

The backend ingests nflverse play-by-play data with `nflreadpy`, cleans fourth-down plays, stores them in PostgreSQL, and exposes FastAPI endpoints for summaries, historical recommendations, ML-based EPA predictions, email auth, and a C++ possession simulator (with Python fallback).

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
- passlib / python-jose (auth)
- pybind11 (optional C++ simulator)

## Setup

### Database & tables

```bash
cd backend
pip install -r requirements-core.txt
# Set DATABASE_URL and SECRET_KEY in .env
python scripts/create_tables.py
```

### C++ simulator (optional)

```bash
cd backend
python setup_sim.py build_ext --inplace
```

See `backend/simulation/README.md`.

### Run API

```bash
uvicorn app.main:app --reload
```

### Run frontend

```bash
cd frontend && npm install && npm run dev
```

## API overview

| Endpoint | Auth | Description |
|----------|------|-------------|
| `POST /recommend` | No | Historical EPA recommendation |
| `POST /recommended/ML` | No | ML EPA (yard line, distance, quarter, clock, score diff) |
| `POST /simulate/possession` | No | Monte Carlo drive simulation |
