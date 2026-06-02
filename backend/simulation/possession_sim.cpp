#include "possession_sim.hpp"

#include <algorithm>
#include <cmath>
#include <random>

namespace nfl4d {

namespace {

double clampd(double v, double lo, double hi) {
    return std::max(lo, std::min(hi, v));
}

int clampi(int v, int lo, int hi) {
    return std::max(lo, std::min(hi, v));
}

double field_goal_make_prob(int yardline_100) {
    int kick_distance = yardline_100 + 17;
    if (kick_distance <= 33) return 0.95;
    if (kick_distance <= 40) return 0.88;
    if (kick_distance <= 48) return 0.75;
    if (kick_distance <= 55) return 0.58;
    if (kick_distance <= 60) return 0.42;
    return 0.25;
}

double go_conversion_prob(int ydstogo, int yardline_100) {
    double base = 0.62 - 0.045 * (ydstogo - 1);
    if (yardline_100 <= 20) base += 0.05;
    if (yardline_100 >= 80) base -= 0.08;
    return clampd(base, 0.12, 0.85);
}

void spend_time(GameState& state, int seconds) {
    state.game_seconds_remaining = std::max(0, state.game_seconds_remaining - seconds);
}

void add_play(SimulationResult& result, int down, const std::string& action,
              const std::string& outcome, int yards, int yardline, int points) {
    result.plays.push_back(PlayEvent{down, action, outcome, yards, yardline, points});
}

bool check_touchdown(GameState& state, SimulationResult& result, int down, const std::string& action) {
    if (state.yardline_100 <= 0) {
        state.yardline_100 = 0;
        state.score_off += 6;
        result.points_scored += 6;
        add_play(result, down, action, "touchdown", 0, 0, 6);
        result.possession_ended = true;
        return true;
    }
    return false;
}

void apply_punt(GameState& state, SimulationResult& result, std::mt19937& rng) {
    std::uniform_int_distribution<int> net_dist(32, 48);
    int net = net_dist(rng);
    state.yardline_100 = clampi(state.yardline_100 + net, 20, 99);
    state.down = 1;
    state.ydstogo = 10;
    add_play(result, 4, "punt", "possession_ended", net, state.yardline_100, 0);
    result.possession_ended = true;
}

void apply_field_goal(GameState& state, SimulationResult& result, std::mt19937& rng) {
    std::uniform_real_distribution<double> uni(0.0, 1.0);
    double make_prob = field_goal_make_prob(state.yardline_100);
    if (uni(rng) < make_prob) {
        state.score_off += 3;
        result.points_scored += 3;
        add_play(result, 4, "field_goal", "good", 0, state.yardline_100, 3);
    } else {
        int miss_spot = clampi(state.yardline_100 + 8, 1, 99);
        state.yardline_100 = miss_spot;
        add_play(result, 4, "field_goal", "no_good", 0, miss_spot, 0);
    }
    result.possession_ended = true;
}

void apply_go(GameState& state, SimulationResult& result, std::mt19937& rng) {
    std::uniform_real_distribution<double> uni(0.0, 1.0);
    std::uniform_int_distribution<int> bonus(0, 3);
    if (uni(rng) < go_conversion_prob(state.ydstogo, state.yardline_100)) {
        int yards = state.ydstogo + bonus(rng);
        state.yardline_100 -= yards;
        state.down = 1;
        state.ydstogo = std::min(10, state.yardline_100);
        if (state.ydstogo <= 0) state.ydstogo = 1;
        add_play(result, 4, "go", "converted", yards, state.yardline_100, 0);
        if (check_touchdown(state, result, 4, "go")) return;
    } else {
        add_play(result, 4, "go", "turnover_on_downs", 0, state.yardline_100, 0);
        result.possession_ended = true;
    }
}

void simulate_scrimmage(GameState& state, SimulationResult& result, std::mt19937& rng) {
    std::normal_distribution<double> gain_dist(4.6, 6.5);
    std::uniform_real_distribution<double> uni(0.0, 1.0);

    int yards = static_cast<int>(std::round(std::max(-3.0, gain_dist(rng))));
    spend_time(state, 35);

    if (uni(rng) < 0.025) {
        add_play(result, state.down, "pass", "interception", 0, state.yardline_100, 0);
        result.possession_ended = true;
        return;
    }

    if (uni(rng) < 0.012) {
        add_play(result, state.down, "run", "fumble_lost", 0, state.yardline_100, 0);
        result.possession_ended = true;
        return;
    }

    state.yardline_100 -= yards;

    if (yards >= state.ydstogo) {
        state.down = 1;
        state.ydstogo = std::min(10, state.yardline_100);
        if (state.ydstogo <= 0) state.ydstogo = 1;
        add_play(result, state.down, "play", "first_down", yards, state.yardline_100, 0);
        if (check_touchdown(state, result, state.down, "play")) return;
    } else {
        state.ydstogo -= yards;
        if (state.ydstogo <= 0) state.ydstogo = 1;
        state.down += 1;
        add_play(result, state.down - 1, "play", "gain", yards, state.yardline_100, 0);
        if (state.down > 3) {
            add_play(result, 4, "play", "turnover_on_downs", 0, state.yardline_100, 0);
            result.possession_ended = true;
        }
    }
}

}  // namespace

SimulationResult simulate_possession(
    GameState state,
    const std::string& fourth_decision,
    int seed,
    int max_plays
) {
    SimulationResult result;
    result.final_score_off = state.score_off;
    result.final_score_def = state.score_def;
    result.final_yardline_100 = state.yardline_100;
    result.possession_ended = false;

    std::mt19937 rng(static_cast<unsigned>(seed));

    state.down = 4;
    spend_time(state, 40);

    if (fourth_decision == "punt") {
        apply_punt(state, result, rng);
    } else if (fourth_decision == "field_goal") {
        apply_field_goal(state, result, rng);
    } else {
        apply_go(state, result, rng);
    }

    int play_count = static_cast<int>(result.plays.size());
    while (!result.possession_ended && play_count < max_plays && state.game_seconds_remaining > 0) {
        if (state.yardline_100 <= 25 && state.down <= 3) {
            std::uniform_real_distribution<double> uni(0.0, 1.0);
            if (uni(rng) < 0.18) {
                apply_field_goal(state, result, rng);
                break;
            }
        }
        simulate_scrimmage(state, result, rng);
        play_count = static_cast<int>(result.plays.size());
    }

    result.final_score_off = state.score_off;
    result.final_score_def = state.score_def;
    result.final_yardline_100 = state.yardline_100;
    return result;
}

}  // namespace nfl4d
