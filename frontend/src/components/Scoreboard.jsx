import { formatClock, formatQuarter, formatScoreDiff, scoreDifferential } from "../utils/game";

function formatDown(down) {
  if (down === 1) return "1st";
  if (down === 2) return "2nd";
  if (down === 3) return "3rd";
  return "4th";
}

export default function Scoreboard({
  qtr = 4,
  clockMinutes = 15,
  clockSeconds = 0,
  scoreOff = 0,
  scoreDef = 0,
  yardline100,
  ydstogo,
  down = 4,
}) {
  const diff = scoreDifferential(scoreOff, scoreDef);

  return (
    <div className="scoreboard" aria-label="Game scoreboard">
      <div className="scoreboard-clock">
        <span className="scoreboard-qtr">{formatQuarter(qtr)}</span>
        <span className="scoreboard-time">{formatClock(clockMinutes, clockSeconds)}</span>
      </div>
      <div className="scoreboard-scores">
        <div className="scoreboard-team scoreboard-team--off">
          <span className="scoreboard-team-label">OFF</span>
          <span className="scoreboard-team-score">{scoreOff}</span>
        </div>
        <span className="scoreboard-vs">–</span>
        <div className="scoreboard-team scoreboard-team--def">
          <span className="scoreboard-team-label">DEF</span>
          <span className="scoreboard-team-score">{scoreDef}</span>
        </div>
      </div>
      <div className="scoreboard-situation">
        <span>{formatDown(down)} &amp; {ydstogo}</span>
        <span className="scoreboard-dot">·</span>
        <span>Opp {yardline100}</span>
        <span className="scoreboard-dot">·</span>
        <span className={diff > 0 ? "positive" : diff < 0 ? "negative" : ""}>
          {formatScoreDiff(diff)}
        </span>
      </div>
    </div>
  );
}
