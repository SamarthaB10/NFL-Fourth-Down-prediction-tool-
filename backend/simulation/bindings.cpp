#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "possession_sim.hpp"

namespace py = pybind11;

PYBIND11_MODULE(nfl4d_sim, m) {
    m.doc() = "C++ possession simulator for NFL 4D";

    py::class_<nfl4d::PlayEvent>(m, "PlayEvent")
        .def_readonly("down", &nfl4d::PlayEvent::down)
        .def_readonly("action", &nfl4d::PlayEvent::action)
        .def_readonly("outcome", &nfl4d::PlayEvent::outcome)
        .def_readonly("yards_gained", &nfl4d::PlayEvent::yards_gained)
        .def_readonly("yardline_100", &nfl4d::PlayEvent::yardline_100)
        .def_readonly("points", &nfl4d::PlayEvent::points);

    py::class_<nfl4d::SimulationResult>(m, "SimulationResult")
        .def_readonly("points_scored", &nfl4d::SimulationResult::points_scored)
        .def_readonly("final_score_off", &nfl4d::SimulationResult::final_score_off)
        .def_readonly("final_score_def", &nfl4d::SimulationResult::final_score_def)
        .def_readonly("final_yardline_100", &nfl4d::SimulationResult::final_yardline_100)
        .def_readonly("possession_ended", &nfl4d::SimulationResult::possession_ended)
        .def_readonly("plays", &nfl4d::SimulationResult::plays);

    m.def(
        "simulate_possession",
        [](int yardline_100, int ydstogo, int qtr, int game_seconds_remaining,
           int score_off, int score_def, const std::string& decision, int seed) {
            nfl4d::GameState state;
            state.yardline_100 = yardline_100;
            state.ydstogo = ydstogo;
            state.qtr = qtr;
            state.game_seconds_remaining = game_seconds_remaining;
            state.score_off = score_off;
            state.score_def = score_def;
            return nfl4d::simulate_possession(state, decision, seed);
        },
        py::arg("yardline_100"),
        py::arg("ydstogo"),
        py::arg("qtr") = 4,
        py::arg("game_seconds_remaining") = 900,
        py::arg("score_off") = 0,
        py::arg("score_def") = 0,
        py::arg("decision"),
        py::arg("seed") = 42
    );
}
