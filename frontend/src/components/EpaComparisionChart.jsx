import { formatDecision, formatEpa } from "../utils/format";

const OPTION_KEYS = ["go", "punt", "field_goal"];

export default function EpaComparisonChart({ data, highlightKey, valueLabel = "Avg EPA" }) {
  if (!data) return null;

  const entries = OPTION_KEYS.map((key) => ({
    key,
    label: formatDecision(key),
    value: data[key]?.avgEpa ?? data[key] ?? null,
  })).filter((e) => e.value !== null && e.value !== undefined);

  if (entries.length === 0) return null;

  const maxAbs = Math.max(...entries.map((e) => Math.abs(e.value)), 0.01);

  return (
    <div className="epa-chart">
      <h3 className="epa-chart-title">{valueLabel}</h3>
      <ul className="epa-chart-bars">
        {entries.map(({ key, label, value }) => (
          <li key={key} className={highlightKey === key ? "epa-bar-row--highlight" : ""}>
            <span className="epa-bar-label">{label}</span>
            <div className="epa-bar-track">
              <div
                className={`epa-bar-fill ${value >= 0 ? "positive" : "negative"}`}
                style={{ width: `${(Math.abs(value) / maxAbs) * 100}%` }}
              />
            </div>
            <span className={`epa-bar-value ${value > 0 ? "positive" : value < 0 ? "negative" : ""}`}>
              {formatEpa(value)}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
