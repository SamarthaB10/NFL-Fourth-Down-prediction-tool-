import { Link } from "react-router-dom";
import lamarJackson from "../assets/lamar-jackson.png";

const FEATURES = [
  {
    title: "Historical EPA",
    text: "Match similar 4th-down situations from prior seasons and compare average EPA by decision.",
    to: "/tool",
    cta: "View history",
  },
  {
    title: "ML predictions",
    text: "XGBoost models use yard line, distance, quarter, game clock, and score differential.",
    to: "/tool",
    state: { tab: "ml" },
    cta: "Run ML",
  },
  {
    title: "Play explorer",
    text: "Browse real 4th-down plays with teams, yard line, and EPA.",
    to: "/plays",
    cta: "Browse plays",
  },
  {
    title: "Season dashboard",
    text: "Season-level decision rates and average EPA by choice.",
    to: "/dashboard",
    cta: "View seasons",
  },
];

export default function Home() {
  return (
    <div className="home-page">
      <section className="home-hero">
        <div className="home-hero-content">
          <h2 className="home-hero-title">
            Smarter <span className="highlight">4th down</span> decisions
          </h2>
          <p className="home-hero-text">
            Historical data and ML with full game context: quarter, clock,
            score, field position, and yards to go.
          </p>
          <div className="home-hero-actions">
            <Link to="/tool" className="btn-primary btn-primary--inline">
              Open decision tool
            </Link>
            <Link to="/plays" className="btn-retry">
              Browse plays
            </Link>
          </div>
        </div>
        <img src={lamarJackson} alt="" className="home-hero-image" />
      </section>

      <section className="home-features">
        {FEATURES.map(({ title, text, to, state, cta }) => (
          <Link key={title} to={to} state={state} className="feature-card">
            <h3>{title}</h3>
            <p>{text}</p>
            <span className="feature-card-link">{cta} →</span>
          </Link>
        ))}
      </section>

      <section className="home-steps">
        <h3 className="home-steps-title">How it works</h3>
        <ol className="steps-list">
          <li>
            <strong>Set game context</strong> — field position, distance, quarter, clock, and score.
          </li>
          <li>
            <strong>Historical or ML</strong> — compare observed EPA or model-predicted EPA for each option.
          </li>
          <li>
            <strong>Decide with data</strong> — charts, model outputs, and real play logs.
          </li>
        </ol>
      </section>
    </div>
  );
}
