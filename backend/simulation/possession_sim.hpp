#pragma once

#include <string>
#include <vector>

namespace nfl4d {

struct GameState {
    int yardline_100 = 50;
    int ydstogo = 10;
    int down = 1;
    int qtr = 4;
    int game_seconds_remaining = 900;
    int score_off = 0;
    int score_def = 0;
};

struct PlayEvent {
    int down = 0;
    std::string action;
    std::string outcome;
    int yards_gained = 0;
    int yardline_100 = 0;
    int points = 0;
};

struct SimulationResult {
    int points_scored = 0;
    int final_score_off = 0;
    int final_score_def = 0;
    int final_yardline_100 = 50;
    bool possession_ended = true;
    std::vector<PlayEvent> plays;
};

SimulationResult simulate_possession(
    GameState state,
    const std::string& fourth_decision,
    int seed,
    int max_plays = 30
);

}  // namespace nfl4d
