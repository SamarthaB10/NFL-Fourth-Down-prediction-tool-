import sys
import types

import pandas as pd
import pytest

from app.services.pbp_cache import load_pbp_from_cache, pbp_cache_path


def test_load_pbp_from_cache_reads_local_file(monkeypatch, tmp_path):
    monkeypatch.setenv("PBP_CACHE_DIR", str(tmp_path))
    cached = pd.DataFrame([{"season": 2024, "play_id": 1}])
    cached.to_pickle(pbp_cache_path(2024))

    loaded = load_pbp_from_cache(2024)

    pd.testing.assert_frame_equal(loaded, cached)


def test_load_pbp_from_cache_does_not_fetch_by_default(monkeypatch, tmp_path):
    monkeypatch.setenv("PBP_CACHE_DIR", str(tmp_path))

    with pytest.raises(FileNotFoundError):
        load_pbp_from_cache(2024)


def test_load_pbp_from_cache_fetches_only_when_allowed(monkeypatch, tmp_path):
    monkeypatch.setenv("PBP_CACHE_DIR", str(tmp_path))
    fetched = pd.DataFrame([{"season": 2024, "play_id": 7}])

    class FakePbp:
        def to_pandas(self):
            return fetched

    fake_nflreadpy = types.SimpleNamespace(load_pbp=lambda seasons: FakePbp())
    monkeypatch.setitem(sys.modules, "nflreadpy", fake_nflreadpy)

    loaded = load_pbp_from_cache(2024, allow_fetch=True)
    reloaded = load_pbp_from_cache(2024)

    pd.testing.assert_frame_equal(loaded, fetched)
    pd.testing.assert_frame_equal(reloaded, fetched)
