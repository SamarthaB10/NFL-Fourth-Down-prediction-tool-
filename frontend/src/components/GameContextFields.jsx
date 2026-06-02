import { formatScoreDiff, scoreDifferential } from "../utils/game";

export default function GameContextFields({ values, onChange }) {
  const handleChange = (e) => {
    const { name, value } = e.target;
    const numeric = ["qtr", "clockMinutes", "clockSeconds", "score_off", "score_def"];
    onChange({
      ...values,
      [name]: numeric.includes(name) ? parseInt(value, 10) || 0 : value,
    });
  };

  const diff = scoreDifferential(values.score_off, values.score_def);

  return (
    <div className="game-context-fields">
      <p className="field-section-label">Game situation</p>
      <div className="input-row">
        <div className="input-group">
          <label htmlFor="qtr">Quarter</label>
          <select id="qtr" name="qtr" value={values.qtr ?? 4} onChange={handleChange}>
            <option value={1}>1st</option>
            <option value={2}>2nd</option>
            <option value={3}>3rd</option>
            <option value={4}>4th</option>
            <option value={5}>Overtime</option>
          </select>
        </div>
        <div className="input-group">
          <label>Time remaining</label>
          <div className="clock-row">
            <input
              name="clockMinutes"
              type="number"
              min={0}
              max={15}
              value={values.clockMinutes ?? 15}
              onChange={handleChange}
              aria-label="Minutes"
            />
            <span className="clock-sep">:</span>
            <input
              name="clockSeconds"
              type="number"
              min={0}
              max={59}
              value={values.clockSeconds ?? 0}
              onChange={handleChange}
              aria-label="Seconds"
            />
          </div>
        </div>
      </div>
      <div className="input-row">
        <div className="input-group">
          <label htmlFor="score_off">Your score</label>
          <input
            id="score_off"
            name="score_off"
            type="number"
            min={0}
            max={100}
            value={values.score_off ?? 0}
            onChange={handleChange}
          />
        </div>
        <div className="input-group">
          <label htmlFor="score_def">Opponent score</label>
          <input
            id="score_def"
            name="score_def"
            type="number"
            min={0}
            max={100}
            value={values.score_def ?? 0}
            onChange={handleChange}
          />
        </div>
      </div>
      <p className="score-diff-hint">
        Score differential (for ML):{" "}
        <strong className={diff > 0 ? "positive" : diff < 0 ? "negative" : ""}>
          {formatScoreDiff(diff)}
        </strong>
      </p>
    </div>
  );
}
