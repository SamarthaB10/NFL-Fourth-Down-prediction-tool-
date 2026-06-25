import pandas as pd
import pytest

from app.services.data_cleaning import clean_down_plays, clean_early_down_plays, clean_fourth_down_plays


def _fake_pbp():
    return pd.DataFrame(
        {
            "down": [1, 2, 3, 4, 4, 4, 3, 1],
            "play_type": [
                "run",
                "pass",
                "run",
                "pass",
                "punt",
                "field_goal",
                "no_play",
                None,
            ],
            "epa": [0.3, 0.7, 0.1, 1.2, -0.1, 0.3, 0.0, None],
        }
    )


def test_clean_down_plays_keeps_first_second_and_third_down_choices():
    result = clean_early_down_plays(_fake_pbp())

    assert result["down"].tolist() == [1, 2, 3]
    assert result["decision"].tolist() == ["run", "pass", "run"]


def test_clean_down_plays_can_select_multiple_downs():
    result = clean_down_plays(_fake_pbp(), [2, 4])

    assert result["down"].tolist() == [2, 4, 4, 4]
    assert result["decision"].tolist() == ["pass", "pass", "punt", "field_goal"]


def test_clean_fourth_down_plays_preserves_existing_go_grouping():
    result = clean_fourth_down_plays(_fake_pbp())

    assert result["down"].tolist() == [4, 4, 4]
    assert result["decision"].tolist() == ["go", "punt", "field_goal"]


def test_clean_down_plays_rejects_invalid_downs():
    with pytest.raises(ValueError):
        clean_down_plays(_fake_pbp(), [0, 5])
