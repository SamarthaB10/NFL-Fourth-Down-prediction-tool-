import { formatDecision, formatEpa } from "../utils/format";
import { formatClock, formatQuarter, formatScoreDiff } from "../utils/game";
import EpaComparisonChart from "./EpaComparisionChart";

const OPTION_KEYS = ["go", "punt", "field_goal"];

export default function RecommendationCard({ result, title = "Recommendation" }) {
  if (!result) return null;

  if (result.message && !result.recommendation) {
    return (
      <div className="error-card">
        <h3>No data found</h3>
        <p>{result.message}</p>
      </div>
    );
  }

  return (
    <div className="recommendation-card">
      <div className="card-header-flex">
        <h2>{title}</h2>
        {result.historical_context && (
          <span className="sample-size-badge">
            {result.historical_context.similarPlays} similar plays
          </span>
        )}
      </div>

      <div className="master-verdict">
        <span className="verdict-label">Optimal choice</span>
        <span className={`verdict-value verdict-${result.recommendation}`}>
          {formatDecision(result.recommendation)}
        </span>
      </div>

      <EpaComparisonChart
        data={result.options}
        highlightKey={result.recommendation}
      />

      <div className="options-table-container">
        <h3>Breakdown</h3>
        <table className="options-table">
          <thead>
            <tr>
              <th>Option</th>
              <th>Plays</th>
              <th>Avg EPA</th>
            </tr>
          </thead>
          <tbody>
            {OPTION_KEYS.map((key) => {
              const opt = result.options?.[key];
              if (!opt) return null;
              return (
                <tr
                  key={key}
                  className={result.recommendation === key ? "highlighted-row" : ""}
                >
                  <td className="option-name">{formatDecision(key)}</td>
                  <td>{opt.count}</td>
                  <td
                    className={`epa-cell ${
                      opt.avgEpa > 0 ? "positive" : opt.avgEpa < 0 ? "negative" : ""
                    }`}
                  >
                    {formatEpa(opt.avgEpa)}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export function MLRecommendationCard({ result }) {
  if (!result) return null;

  const inp = result.input;
  const coachDecision = result.Historical_coach_decision ?? result.coach_decision;
  const chartData = {
    go: { avgEpa: result.predicted_epa?.go },
    punt: { avgEpa: result.predicted_epa?.punt },
    field_goal: { avgEpa: result.predicted_epa?.field_goal },
  };
  const coachProbabilities = coachDecision?.probabilities ?? {};

  const clock = inp?.game_seconds_remaining != null
    ? formatClock(Math.floor(inp.game_seconds_remaining / 60), inp.game_seconds_remaining % 60)
    : null;

  return (
    <div className="recommendation-card">
      <div className="card-header-flex">
        <h2>ML prediction</h2>
        <span className="sample-size-badge sample-size-badge--ml">XGBoost · 5 features</span>
      </div>

      {inp && (
        <div className="context-pills">
          <span className="context-pill">{formatQuarter(inp.qtr)}</span>
          {clock && <span className="context-pill">{clock}</span>}
          <span className="context-pill">
            {inp.yardline_100} yd line · 4th &amp; {inp.ydstogo}
          </span>
          <span
            className={`context-pill ${
              inp.score_differential > 0
                ? "context-pill--pos"
                : inp.score_differential < 0
                  ? "context-pill--neg"
                  : ""
            }`}
          >
            Score diff {formatScoreDiff(inp.score_differential)}
          </span>
        </div>
      )}

      <div className="master-verdict">
        <span className="verdict-label">Model choice</span>
        <span className={`verdict-value verdict-${result.recommendation}`}>
          {formatDecision(result.recommendation)}
        </span>
      </div>

      <EpaComparisonChart
        data={chartData}
        highlightKey={result.recommendation}
        valueLabel="Predicted EPA"
      />

      {coachDecision && (
        <div className="coach-comparison">
          <div className="coach-comparison__header">
            <div>
              <h3>Coach classifier</h3>
              <p>Historical coach behavior for this same situation</p>
            </div>
            <span className={`coach-decision verdict-${coachDecision.decision}`}>
              {formatDecision(coachDecision.decision)}
            </span>
          </div>

          <div className="coach-model-grid">
            <div className="coach-model-card">
              <span className="coach-model-label">EPA model</span>
              <strong className={`verdict-${result.recommendation}`}>
                {formatDecision(result.recommendation)}
              </strong>
            </div>
            <div className="coach-model-card">
              <span className="coach-model-label">Historical coach</span>
              <strong className={`verdict-${coachDecision.decision}`}>
                {formatDecision(coachDecision.decision)}
              </strong>
            </div>
          </div>

          <div className="coach-probabilities" aria-label="Coach decision probabilities">
            {OPTION_KEYS.map((key) => {
              const probability = coachProbabilities[key] ?? 0;
              const percent = Math.round(probability * 100);

              return (
                <div className="coach-probability-row" key={key}>
                  <div className="coach-probability-meta">
                    <span>{formatDecision(key)}</span>
                    <strong>{percent}%</strong>
                  </div>
                  <div className="coach-probability-track">
                    <div
                      className={`coach-probability-fill coach-probability-fill--${key}`}
                      style={{ width: `${percent}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
