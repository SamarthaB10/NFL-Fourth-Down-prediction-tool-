import GameContextFields from "./GameContextFields";

const NFL_TEAMS = [
  "ARI", "ATL", "BAL", "BUF", "CAR", "CHI", "CIN", "CLE",
  "DAL", "DEN", "DET", "GB", "HOU", "IND", "JAX", "KC",
  "LV", "LAC", "LAR", "MIA", "MIN", "NE", "NO", "NYG",
  "NYJ", "PHI", "PIT", "SEA", "SF", "TB", "TEN", "WAS",
];

const CURRENT_YEAR = new Date().getFullYear();

export default function RecommendationForm({
  values,
  onChange,
  onSubmit,
  loading,
  mode = "historical",
}) {
  const handleChange = (e) => {
    const { name, value } = e.target;
    const numericFields = ["yardline_100", "ydstogo", "season"];
    onChange({
      ...values,
      [name]: numericFields.includes(name) ? parseInt(value, 10) || 0 : value,
    });
  };

  const seasonOptions = [CURRENT_YEAR, CURRENT_YEAR - 1, CURRENT_YEAR - 2].map((y) => (
    <option key={y} value={y}>
      Before {y} season
    </option>
  ));

  return (
    <form className="input-card" onSubmit={onSubmit}>
      <h2>{mode === "ml" ? "ML game scenario" : "Historical scenario"}</h2>
      {mode === "ml" && (
        <p className="form-hint">
          Models use field position, distance, quarter, clock, and score differential.
        </p>
      )}

      {mode === "historical" && (
        <div className="input-group">
          <label htmlFor="season">Historical cutoff season</label>
          <select id="season" name="season" value={values.season} onChange={handleChange}>
            {seasonOptions}
          </select>
        </div>
      )}

      <p className="field-section-label">Field position</p>
      <div className="input-row">
        <div className="input-group">
          <label htmlFor="yardline_100">Yards to opponent end zone</label>
          <input
            id="yardline_100"
            type="number"
            name="yardline_100"
            min={1}
            max={99}
            value={values.yardline_100}
            onChange={handleChange}
          />
        </div>
        <div className="input-group">
          <label htmlFor="ydstogo">Yards to go</label>
          <input
            id="ydstogo"
            type="number"
            name="ydstogo"
            min={1}
            max={99}
            value={values.ydstogo}
            onChange={handleChange}
          />
        </div>
      </div>

      {mode === "ml" && <GameContextFields values={values} onChange={onChange} />}

      {mode === "historical" && (
        <div className="input-row">
          <div className="input-group">
            <label htmlFor="posteam">Offense (optional)</label>
            <input
              id="posteam"
              type="text"
              name="posteam"
              list="nfl-teams"
              placeholder="e.g. KC"
              maxLength={3}
              value={values.posteam}
              onChange={handleChange}
            />
          </div>
          <div className="input-group">
            <label htmlFor="defteam">Defense (optional)</label>
            <input
              id="defteam"
              type="text"
              name="defteam"
              list="nfl-teams"
              placeholder="e.g. SF"
              maxLength={3}
              value={values.defteam}
              onChange={handleChange}
            />
          </div>
          <datalist id="nfl-teams">
            {NFL_TEAMS.map((t) => (
              <option key={t} value={t} />
            ))}
          </datalist>
        </div>
      )}

      <button type="submit" className="btn-primary" disabled={loading}>
        {loading ? "Calculating…" : mode === "ml" ? "Run ML prediction" : "Get recommendation"}
      </button>
    </form>
  );
}
