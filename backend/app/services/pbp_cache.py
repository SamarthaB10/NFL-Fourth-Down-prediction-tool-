"""Cache-first access to NFL play-by-play data."""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd


DEFAULT_CACHE_DIR = Path(__file__).resolve().parents[2] / ".cache" / "pbp"


def _cache_dir() -> Path:
    return Path(os.getenv("PBP_CACHE_DIR", DEFAULT_CACHE_DIR))


def pbp_cache_path(season: int) -> Path:
    return _cache_dir() / f"pbp_{season}.pkl"


def load_pbp_from_cache(
    season: int,
    *,
    allow_fetch: bool = False,
    refresh: bool = False,
) -> pd.DataFrame:
    """Load play-by-play data from local cache, fetching only when explicit."""
    cache_path = pbp_cache_path(season)
    if cache_path.exists() and not refresh:
        return pd.read_pickle(cache_path)

    if not allow_fetch:
        raise FileNotFoundError(
            f"No cached PBP data for {season} at {cache_path}. "
            "Run the ingestion script with --fetch to populate the cache."
        )

    import nflreadpy

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    pbp = nflreadpy.load_pbp(seasons=season).to_pandas()
    pbp.to_pickle(cache_path)
    return pbp
