import { useEffect, useState } from "react";
import { getPlays } from "../api/recommendations";
import { formatDecision, formatEpa } from "../utils/format";

export default function SimilarPlays() {
  const [plays, setPlays] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    getPlays()
      .then((data) => {
        if (!cancelled) setPlays(data);
      })
      .catch((err) => {
        if (!cancelled) setError(err.message ?? "Failed to load plays");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div className="plays-page">
      <div className="page-header">
        <h2 className="page-title">Recent 4th down plays</h2>
        <p className="page-subtitle">Sample of plays from the database (latest 50).</p>
      </div>

      {loading && (
        <div className="loading-card">
          <div className="spinner" />
          <p>Loading plays…</p>
        </div>
      )}

      {!loading && error && (
        <div className="error-card">
          <h3>Could not load plays</h3>
          <p>{error}</p>
        </div>
      )}

      {!loading && !error && (
        <div className="plays-table-wrap">
          <table className="options-table plays-table">
            <thead>
              <tr>
                <th>Season</th>
                <th>Wk</th>
                <th>Off</th>
                <th>Def</th>
                <th>Decision</th>
                <th>YTG</th>
                <th>Yard</th>
                <th>EPA</th>
              </tr>
            </thead>
            <tbody>
              {plays.map((play, i) => (
                <tr key={`${play.season}-${play.week}-${i}`}>
                  <td>{play.season}</td>
                  <td>{play.week}</td>
                  <td>{play.posteam}</td>
                  <td>{play.defteam}</td>
                  <td className="option-name">{formatDecision(play.decision)}</td>
                  <td>{play.ydstogo}</td>
                  <td>{play.yardline_100}</td>
                  <td
                    className={`epa-cell ${
                      play.epa > 0 ? "positive" : play.epa < 0 ? "negative" : ""
                    }`}
                  >
                    {formatEpa(play.epa)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {plays.length === 0 && (
            <p className="empty-message">No plays in the database yet.</p>
          )}
        </div>
      )}
    </div>
  );
}
