"""Possession simulation — uses C++ extension when built, else pure Python."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Literal

Decision = Literal["go", "punt", "field_goal"]

try:
    import nfl4d_sim

    _HAS_CPP = True
except ImportError:
    _HAS_CPP = False


@dataclass
class PlayEvent:
    down: int
    action: str
    outcome: str
    yards_gained: int
    yardline_100: int
    points: int


@dataclass
class SimulationResult:
    points_scored: int
    final_score_off: int
    final_score_def: int
    final_yardline_100: int
    possession_ended: bool
    plays: list[PlayEvent] = field(default_factory=list)


def _clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def _fg_prob(yardline_100: int) -> float:
    dist = yardline_100 + 17
    if dist <= 33:
        return 0.95
    if dist <= 40:
        return 0.88
    if dist <= 48:
        return 0.75
    if dist <= 55:
        return 0.58
    if dist <= 60:
        return 0.42
    return 0.25


def _go_prob(ydstogo: int, yardline_100: int) -> float:
    base = 0.62 - 0.045 * (ydstogo - 1)
    if yardline_100 <= 20:
        base += 0.05
    if yardline_100 >= 80:
        base -= 0.08
    return _clamp(base, 0.12, 0.85)


def _python_simulate(
    yardline_100: int,
    ydstogo: int,
    qtr: int,
    game_seconds_remaining: int,
    score_off: int,
    score_def: int,
    decision: str,
    seed: int,
) -> SimulationResult:
    rng = random.Random(seed)
    yl = yardline_100
    ytg = ydstogo
    down = 4
    seconds = game_seconds_remaining
    off, def_ = score_off, score_def
    points = 0
    plays: list[PlayEvent] = []
    ended = False

    def log(d, action, outcome, yards, yline, pts=0):
        plays.append(PlayEvent(d, action, outcome, yards, yline, pts))

    def spend(sec: int):
        nonlocal seconds
        seconds = max(0, seconds - sec)

    def td(d, action):
        nonlocal yl, off, points, ended
        if yl <= 0:
            yl = 0
            off += 6
            points += 6
            log(d, action, "touchdown", 0, 0, 6)
            ended = True
            return True
        return False

    spend(40)
    if decision == "punt":
        net = rng.randint(32, 48)
        yl = min(99, max(20, yl + net))
        log(4, "punt", "possession_ended", net, yl)
        ended = True
    elif decision == "field_goal":
        if rng.random() < _fg_prob(yl):
            off += 3
            points += 3
            log(4, "field_goal", "good", 0, yl, 3)
        else:
            yl = min(99, max(1, yl + 8))
            log(4, "field_goal", "no_good", 0, yl)
        ended = True
    else:
        if rng.random() < _go_prob(ytg, yl):
            yards = ytg + rng.randint(0, 3)
            yl -= yards
            down = 1
            ytg = min(10, max(1, yl))
            log(4, "go", "converted", yards, yl)
            if td(4, "go"):
                return SimulationResult(points, off, def_, yl, True, plays)
        else:
            log(4, "go", "turnover_on_downs", 0, yl)
            ended = True

    while not ended and len(plays) < 30 and seconds > 0:
        if yl <= 25 and down <= 3 and rng.random() < 0.18:
            if rng.random() < _fg_prob(yl):
                off += 3
                points += 3
                log(4, "field_goal", "good", 0, yl, 3)
            else:
                yl = min(99, max(1, yl + 8))
                log(4, "field_goal", "no_good", 0, yl)
            ended = True
            break

        spend(35)
        if rng.random() < 0.025:
            log(down, "pass", "interception", 0, yl)
            ended = True
            break
        if rng.random() < 0.012:
            log(down, "run", "fumble_lost", 0, yl)
            ended = True
            break

        yards = max(-3, int(round(rng.gauss(4.6, 6.5))))
        yl -= yards
        if yards >= ytg:
            down = 1
            ytg = min(10, max(1, yl))
            log(down, "play", "first_down", yards, yl)
            if td(down, "play"):
                break
        else:
            ytg = max(1, ytg - yards)
            down += 1
            log(down - 1, "play", "gain", yards, yl)
            if down > 3:
                log(4, "play", "turnover_on_downs", 0, yl)
                ended = True

    return SimulationResult(points, off, def_, yl, ended, plays)


def _cpp_to_result(raw) -> SimulationResult:
    plays = [
        PlayEvent(p.down, p.action, p.outcome, p.yards_gained, p.yardline_100, p.points)
        for p in raw.plays
    ]
    return SimulationResult(
        raw.points_scored,
        raw.final_score_off,
        raw.final_score_def,
        raw.final_yardline_100,
        raw.possession_ended,
        plays,
    )


def simulate_possession(
    yardline_100: int,
    ydstogo: int,
    decision: Decision,
    qtr: int = 4,
    game_seconds_remaining: int = 900,
    score_off: int = 0,
    score_def: int = 0,
    seed: int = 42,
) -> tuple[SimulationResult, str]:
    if _HAS_CPP:
        raw = nfl4d_sim.simulate_possession(
            yardline_100,
            ydstogo,
            qtr,
            game_seconds_remaining,
            score_off,
            score_def,
            decision,
            seed,
        )
        return _cpp_to_result(raw), "cpp"

    return _python_simulate(
        yardline_100,
        ydstogo,
        qtr,
        game_seconds_remaining,
        score_off,
        score_def,
        decision,
        seed,
    ), "python"


def run_monte_carlo(
    yardline_100: int,
    ydstogo: int,
    decision: Decision,
    trials: int,
    qtr: int = 4,
    game_seconds_remaining: int = 900,
    score_off: int = 0,
    score_def: int = 0,
    seed: int = 42,
) -> dict:
    total_points = 0.0
    touchdowns = 0
    field_goals = 0
    punts = 0
    turnovers = 0
    engine = "python"
    sample: SimulationResult | None = None

    for i in range(trials):
        result, eng = simulate_possession(
            yardline_100,
            ydstogo,
            decision,
            qtr,
            game_seconds_remaining,
            score_off,
            score_def,
            seed + i,
        )
        engine = eng
        if i == 0:
            sample = result
        total_points += result.points_scored
        for play in result.plays:
            if play.outcome == "touchdown":
                touchdowns += 1
            elif play.action == "field_goal" and play.outcome == "good":
                field_goals += 1
            elif play.action == "punt":
                punts += 1
            elif "turnover" in play.outcome or play.outcome == "interception" or play.outcome == "fumble_lost":
                turnovers += 1

    assert sample is not None
    return {
        "engine": engine,
        "trials": trials,
        "mean_points_scored": round(total_points / trials, 3),
        "touchdown_rate": round(touchdowns / trials, 3),
        "field_goal_rate": round(field_goals / trials, 3),
        "punt_rate": round(punts / trials, 3),
        "turnover_rate": round(turnovers / trials, 3),
        "sample": sample,
    }
