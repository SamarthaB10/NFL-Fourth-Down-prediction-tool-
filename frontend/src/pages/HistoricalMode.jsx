import { useState } from "react";
import RecommendationForm from "../components/RecommendationForm";
import RecommendationCard from "../components/RecommendationCard";
import FootballField from "../components/FootballField";
import { getHistoricalRecommendation } from "../api/recommendations";

const CURRENT_YEAR = new Date().getFullYear();

const defaultValues = {
  season: CURRENT_YEAR,
  yardline_100: 45,
  ydstogo: 4,
  posteam: "",
  defteam: "",
};

export default function HistoricalMode() {
  const [values, setValues] = useState(defaultValues);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const data = await getHistoricalRecommendation(values);
      setResult(data);
    } catch (err) {
      setError(err.message ?? "Failed to fetch recommendation");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="tool-grid">
      <aside className="tool-sidebar">
        <RecommendationForm
          values={values}
          onChange={setValues}
          onSubmit={handleSubmit}
          loading={loading}
          mode="historical"
        />
        <FootballField yardline100={values.yardline_100} ydstogo={values.ydstogo} />
      </aside>

      <section className="output-zone">
        {loading && (
          <div className="loading-card">
            <div className="spinner" />
            <p>Scanning historical play database…</p>
          </div>
        )}
        {!loading && error && (
          <div className="error-card">
            <h3>Request failed</h3>
            <p>{error}</p>
          </div>
        )}
        {!loading && !error && result && (
          <RecommendationCard result={result} title="Historical analysis" />
        )}
        {!loading && !error && !result && (
          <div className="placeholder-card">
            <p>Enter a scenario and run historical analysis to see EPA by decision.</p>
          </div>
        )}
      </section>
    </div>
  );
}
