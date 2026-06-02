import { useEffect, useState } from "react";
import { getSeasonSummary } from "../api/recommendations";
import { formatDecision, formatEpa } from "../utils/format";
import EpaComparisonChart from "../components/EpaComparisionChart";

const CURRENT_YEAR = new Date().getFullYear();

export default function TeamDashboard() {
  const [season, setSeason] = useState(CURRENT_YEAR - 1);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const handleSeasonChange = (e) => {
    setSeason(parseInt(e.target.value, 10));
    setLoading(true);
    setError(null);
    setSummary(null);
  };

  useEffect(() => {
    let cancelled = false;
    getSeasonSummary(season)
      .then((data) => {
        if (!cancelled) setSummary(data);
      })
      .catch((err) => {
        if (!cancelled) {
          setError(err.message ?? "Failed to load summary");
          setSummary(null);
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [season]);

  const chartData = summary?.average_epa
    ? {
        go: { avgEpa: summary.average_epa.go },
        punt: { avgEpa: summary.average_epa.punt },
        field_goal: { avgEpa: summary.average_epa.field_goal },
      }
    : null;

  const bestDecision =
    summary?.average_epa &&
    Object.entries(summary.average_epa).sort((a, b) => (b[1] ?? -99) - (a[1] ?? -99))[0]?.[0];

  return (
    <div className="dashboard-page">
      <div className="page-header page-header--row">
        <div>
          <h2 className="page-title">Season dashboard</h2>
          <p className="page-subtitle">Aggregate 4th-down EPA by decision for a full season.</p>
        </div>
        <div className="input-group input-group--inline">
          <label htmlFor="dash-season">Season</label>
          <select
            id="dash-season"
            value={season}
            onChange={handleSeasonChange}
          >
            {[CURRENT_YEAR, CURRENT_YEAR - 1, CURRENT_YEAR - 2, CURRENT_YEAR - 3].map((y) => (
              <option key={y} value={y}>
                {y}
              </option>
            ))}
          </select>
        </div>
      </div>

      {loading && (
        <div className="loading-card">
          <div className="spinner" />
          <p>Loading season data…</p>
        </div>
      )}

      {!loading && error && (
        <div className="error-card">
          <h3>Could not load summary</h3>
          <p>{error}</p>
        </div>
      )}

      {!loading && !error && summary && (
        <div className="dashboard-grid">
          <div className="stat-cards">
            <div className="stat-card">
              <span className="stat-label">Total plays</span>
              <span className="stat-value">{summary.usable_plays ?? summary.total_plays ?? 0}</span>
            </div>
            {summary.message && (
              <div className="error-card stat-card--wide">
                <p>{summary.message}</p>
              </div>
            )}
            {bestDecision && (
              <div className="stat-card stat-card--highlight">
                <span className="stat-label">Highest avg EPA</span>
                <span className="stat-value">{formatDecision(bestDecision)}</span>
              </div>
            )}
          </div>

          {chartData && (
            <div className="recommendation-card">
              <EpaComparisonChart
                data={chartData}
                highlightKey={bestDecision}
                valueLabel={`${season} average EPA`}
              />
              <div className="options-table-container">
                <h3>Decision counts</h3>
                <table className="options-table">
                  <thead>
                    <tr>
                      <th>Decision</th>
                      <th>Count</th>
                      <th>Avg EPA</th>
                    </tr>
                  </thead>
                  <tbody>
                    {Object.entries(summary.decision_counts ?? {}).map(([key, count]) => (
                      <tr key={key}>
                        <td className="option-name">{formatDecision(key)}</td>
                        <td>{count}</td>
                        <td className="epa-cell">
                          {formatEpa(summary.average_epa?.[key])}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
