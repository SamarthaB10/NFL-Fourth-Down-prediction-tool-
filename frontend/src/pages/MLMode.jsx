import { useState } from "react";
import RecommendationForm from "../components/RecommendationForm";
import { MLRecommendationCard } from "../components/RecommendationCard";
import FootballField from "../components/FootballField";
import Scoreboard from "../components/Scoreboard";
import { getMLRecommendation } from "../api/recommendations";
import { scoreDifferential, toGameSeconds } from "../utils/game";

const defaultValues = {
  yardline_100: 45,
  ydstogo: 4,
  qtr: 4,
  clockMinutes: 2,
  clockSeconds: 0,
  score_off: 17,
  score_def: 14,
};

export default function MLMode() {
  const [values, setValues] = useState(defaultValues);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const data = await getMLRecommendation({
        yardline_100: values.yardline_100,
        ydstogo: values.ydstogo,
        qtr: values.qtr,
        game_seconds_remaining: toGameSeconds(values.clockMinutes, values.clockSeconds),
        score_differential: scoreDifferential(values.score_off, values.score_def),
      });
      setResult(data);
    } catch (err) {
      setError(err.message ?? "Failed to fetch ML prediction");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="tool-grid">
      <aside className="tool-sidebar">
        <Scoreboard
          qtr={values.qtr}
          clockMinutes={values.clockMinutes}
          clockSeconds={values.clockSeconds}
          scoreOff={values.score_off}
          scoreDef={values.score_def}
          yardline100={values.yardline_100}
          ydstogo={values.ydstogo}
        />
        <RecommendationForm
          values={values}
          onChange={setValues}
          onSubmit={handleSubmit}
          loading={loading}
          mode="ml"
        />
        <FootballField yardline100={values.yardline_100} ydstogo={values.ydstogo} />
      </aside>

      <section className="output-zone">
        {loading && (
          <div className="loading-card">
            <div className="spinner" />
            <p>Running XGBoost models with game context…</p>
          </div>
        )}
        {!loading && error && (
          <div className="error-card">
            <h3>Request failed</h3>
            <p>{error}</p>
          </div>
        )}
        {!loading && !error && result && <MLRecommendationCard result={result} />}
        {!loading && !error && !result && (
          <div className="placeholder-card">
            <h3>ML prediction mode</h3>
            <p>
              Set quarter, game clock, and score — then run the model to compare predicted EPA
              for go, punt, and field goal.
            </p>
          </div>
        )}
      </section>
    </div>
  );
}
