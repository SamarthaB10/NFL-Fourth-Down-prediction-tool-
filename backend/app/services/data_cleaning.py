"""Cleaning helpers for down-aware play data."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd

STANDARD_DOWNS = (1, 2, 3, 4)
SIMULATION_PLAY_TYPES = ("run", "pass", "punt", "field_goal")
FOURTH_DOWN_DECISIONS = {
    "run": "go",
    "pass": "go",
    "field_goal": "field_goal",
    "punt": "punt",
}


def _normalize_downs(downs: int | Iterable[int] | None) -> list[int]:
    if downs is None:
        return list(STANDARD_DOWNS)
    if isinstance(downs, int):
        normalized = [downs]
    else:
        normalized = list(downs)

    invalid = [down for down in normalized if down not in STANDARD_DOWNS]
    if invalid:
        raise ValueError(f"downs must be between 1 and 4, got {invalid}")
    return normalized


def filter_by_down(pbp: pd.DataFrame, downs: int | Iterable[int] | None = None) -> pd.DataFrame:
    """Return run/pass/punt/field-goal plays for the requested down(s)."""
    selected_downs = _normalize_downs(downs)
    return pbp[
        (pbp["down"].isin(selected_downs))
        & (pbp["play_type"].isin(SIMULATION_PLAY_TYPES))
    ].copy()


def filter_first_downs(pbp: pd.DataFrame) -> pd.DataFrame:
    return filter_by_down(pbp, 1)


def filter_second_downs(pbp: pd.DataFrame) -> pd.DataFrame:
    return filter_by_down(pbp, 2)


def filter_third_downs(pbp: pd.DataFrame) -> pd.DataFrame:
    return filter_by_down(pbp, 3)


def filter_fourth_downs(pbp: pd.DataFrame) -> pd.DataFrame:
    return filter_by_down(pbp, 4)


def add_decision_column(
    pbp: pd.DataFrame,
    *,
    collapse_scrimmage_to_go: bool = False,
) -> pd.DataFrame:
    """Add the model decision label.

    For the existing fourth-down recommender, run/pass stay grouped as ``go``.
    For the simulation tool, run/pass remain separate user-selectable choices.
    """
    plays = pbp.copy()
    if collapse_scrimmage_to_go:
        plays["decision"] = plays["play_type"].replace(FOURTH_DOWN_DECISIONS)
    else:
        plays["decision"] = plays["play_type"]
    return plays


def clean_down_plays(
    pbp: pd.DataFrame,
    downs: int | Iterable[int] | None = None,
) -> pd.DataFrame:
    """Clean standard-down plays for EPA display and simulation choices."""
    return add_decision_column(filter_by_down(pbp, downs))


def clean_early_down_plays(pbp: pd.DataFrame) -> pd.DataFrame:
    return clean_down_plays(pbp, [1, 2, 3])


def clean_fourth_down_plays(pbp: pd.DataFrame) -> pd.DataFrame:
    fourth_downs = filter_fourth_downs(pbp)
    return add_decision_column(fourth_downs, collapse_scrimmage_to_go=True)
