import { useState } from "react";
import { useLocation } from "react-router-dom";
import HistoricalMode from "./HistoricalMode";
import MLMode from "./MLMode";

const TABS = [
  { id: "historical", label: "Historical EPA", desc: "Similar plays from past seasons" },
  { id: "ml", label: "ML prediction", desc: "Quarter, clock & score aware" },
];

function FourthDowntoolInner({ initialTab }) {
  const [tab, setTab] = useState(initialTab ?? "historical");

  return (
    <div className="fourth-down-tool">
      <div className="page-header">
        <h2 className="page-title">4th Down Decision Tool</h2>
        <p className="page-subtitle">
          Historical EPA lookup and ML predictions with full game context for
          your 4th-down call.
        </p>
      </div>

      <div className="mode-tabs mode-tabs--wide" role="tablist">
        {TABS.map(({ id, label, desc }) => (
          <button
            key={id}
            type="button"
            role="tab"
            aria-selected={tab === id}
            className={`mode-tab mode-tab--stacked${tab === id ? " mode-tab--active" : ""}`}
            onClick={() => setTab(id)}
          >
            <span className="mode-tab-label">{label}</span>
            <span className="mode-tab-desc">{desc}</span>
          </button>
        ))}
      </div>

      {tab === "historical" && <HistoricalMode />}
      {tab === "ml" && <MLMode />}
    </div>
  );
}

export default function FourthDowntool() {
  const location = useLocation();
  const navKey = location.state?.tab ?? "";

  return (
    <FourthDowntoolInner
      key={navKey}
      initialTab={location.state?.tab}
    />
  );
}
