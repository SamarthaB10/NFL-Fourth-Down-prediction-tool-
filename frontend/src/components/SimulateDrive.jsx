import { useState } from "react";
import { simulatePossession } from "../api/recommendations";
import DecisionPicker from "./DecisionPicker";
import FootballField from "./FootballField";
import GameContextFields from "./GameContextFields";
import Scoreboard from "./Scoreboard";
import { formatDecision } from "../utils/format";
import { toGameSeconds } from "../utils/game";

const defaultState = {
  yardline_100: 38,
  ydstogo: 4,
  qtr: 4,
  clockMinutes: 2,
  clockSeconds: 0,
  score_off: 17,
  score_def: 14,
  decision: "go",
  trials: 200,
};

export default function SimulateDrive({ compact = false, initialDecision }) {
  const [state, setState] = useState({
    ...defaultState,
    decision: initialDecision ?? defaultState.decision,
  });
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFieldChange = (e) => {
    const { name, value } = e.target;
    const numeric = ["yardline_100", "ydstogo", "trials"];
    setState((prev) => ({
      ...prev,
      [name]: numeric.includes(name) ? parseInt(value, 10) || 0 : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const data = await simulatePossession({
        yardline_100: state.yardline_100,
        ydstogo: state.ydstogo,
        qtr: state.qtr,
        game_seconds_remaining: toGameSeconds(state.clockMinutes, state.clockSeconds),
        score_off: state.score_off,
        score_def: state.score_def,
        decision: state.decision,
        trials: state.trials,
      });
      setResult(data);
    } catch (err) {
      setError(err.message ?? "Simulation failed");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={compact ? "simulate-drive simulate-drive--compact" : "simulate-drive"}>
      {!compact && (
        <div className="page-header">
          <h2 className="page-title">Possession simulator</h2>
          <p className="page-subtitle">
            Choose go, punt, or field goal — the engine plays out the rest of the drive and
            estimates scoring (C++ when built, Python fallback otherwise).
          </p>
        </div>
      )}

      <div className="tool-grid">
        <aside className="tool-sidebar">
          <Scoreboard
            qtr={state.qtr}
            clockMinutes={state.clockMinutes}
            clockSeconds={state.clockSeconds}
            scoreOff={state.score_off}
            scoreDef={state.score_def}
            yardline100={state.yardline_100}
            ydstogo={state.ydstogo}
          />
          <form className="input-card" onSubmit={handleSubmit}>
            <h2>4th down scenario</h2>
            <DecisionPicker
              value={state.decision}
              onChange={(decision) => setState((prev) => ({ ...prev, decision }))}
            />
            <div className="input-row">
              <div className="input-group">
                <label htmlFor="sim-yardline">Yards to opponent EZ</label>
                <input
                  id="sim-yardline"
                  name="yardline_100"
                  type="number"
                  min={1}
                  max={99}
                  value={state.yardline_100}
                  onChange={handleFieldChange}
                />
              </div>
              <div className="input-group">
                <label htmlFor="sim-ytg">Yards to go</label>
                <input
                  id="sim-ytg"
                  name="ydstogo"
                  type="number"
                  min={1}
                  max={30}
                  value={state.ydstogo}
                  onChange={handleFieldChange}
                />
              </div>
            </div>
            <GameContextFields values={state} onChange={setState} />
            <div className="input-group">
              <label htmlFor="trials">Monte Carlo trials</label>
              <input
                id="trials"
                name="trials"
                type="range"
                min={50}
                max={2000}
                step={50}
                value={state.trials}
                onChange={handleFieldChange}
              />
              <span className="range-value">{state.trials} runs</span>
            </div>
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? `Simulating ${state.trials} drives…` : `Simulate ${formatDecision(state.decision)}`}
            </button>
          </form>
          <FootballField yardline100={state.yardline_100} ydstogo={state.ydstogo} />
        </aside>

        <section className="output-zone">
          {loading && (
            <div className="loading-card">
              <div className="spinner" />
              <p>Running {state.trials} possession simulations…</p>
            </div>
          )}
          {!loading && error && (
            <div className="error-card">
              <h3>Simulation failed</h3>
              <p>{error}</p>
            </div>
          )}
          {!loading && !error && !result && (
            <div className="placeholder-card">
              <p>
                Set the situation, pick your 4th-down call, and run the simulator to see expected
                points and a sample drive log.
              </p>
            </div>
          )}
          {!loading && !error && result && (
            <SimulationResults result={result} decision={state.decision} />
          )}
        </section>
      </div>
    </div>
  );
}

function SimulationResults({ result, decision }) {
  return (
    <div className="recommendation-card">
      <div className="card-header-flex">
        <h2>Simulation results</h2>
        <span className="sample-size-badge">
          {result.engine.toUpperCase()} · {result.trials} trials · {formatDecision(decision)}
        </span>
      </div>

      <div className="stat-cards">
        <div className="stat-card stat-card--highlight">
          <span className="stat-label">Avg points this drive</span>
          <span className="stat-value">{result.mean_points_scored}</span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Sample final score</span>
          <span className="stat-value">
            {result.sample_final_score_off}–{result.sample_final_score_def}
          </span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Points on sample drive</span>
          <span className="stat-value">+{result.sample_points_scored}</span>
        </div>
      </div>

      <div className="sim-rates">
        <div className="rate-chip">
          <span className="rate-label">TD</span>
          <span className="rate-value">{(result.touchdown_rate * 100).toFixed(1)}%</span>
        </div>
        <div className="rate-chip">
          <span className="rate-label">FG</span>
          <span className="rate-value">{(result.field_goal_rate * 100).toFixed(1)}%</span>
        </div>
        <div className="rate-chip">
          <span className="rate-label">Punt</span>
          <span className="rate-value">{(result.punt_rate * 100).toFixed(1)}%</span>
        </div>
        <div className="rate-chip">
          <span className="rate-label">Turnover</span>
          <span className="rate-value">{(result.turnover_rate * 100).toFixed(1)}%</span>
        </div>
      </div>

      <div className="options-table-container">
        <h3>Sample drive play-by-play</h3>
        <table className="options-table">
          <thead>
            <tr>
              <th>Down</th>
              <th>Action</th>
              <th>Outcome</th>
              <th>Yds</th>
              <th>Spot</th>
              <th>Pts</th>
            </tr>
          </thead>
          <tbody>
            {result.sample_plays.map((play, i) => (
              <tr key={i} className={play.points > 0 ? "highlighted-row" : ""}>
                <td>{play.down}</td>
                <td className="option-name">{play.action}</td>
                <td>{play.outcome}</td>
                <td>{play.yards_gained}</td>
                <td>{play.yardline_100}</td>
                <td className={play.points > 0 ? "epa-cell positive" : ""}>{play.points}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
