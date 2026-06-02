import { formatDecision } from "../utils/format";

const DECISIONS = ["go", "punt", "field_goal"];

export default function DecisionPicker({ value, onChange, label = "Your 4th down call" }) {
  return (
    <div className="decision-picker-wrap">
      <p className="field-section-label">{label}</p>
      <div className="decision-picker" role="group" aria-label={label}>
        {DECISIONS.map((d) => (
          <button
            key={d}
            type="button"
            className={`decision-btn decision-btn--${d}${
              value === d ? " decision-btn--active" : ""
            }`}
            onClick={() => onChange(d)}
            aria-pressed={value === d}
          >
            {formatDecision(d)}
          </button>
        ))}
      </div>
    </div>
  );
}
