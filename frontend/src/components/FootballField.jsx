export default function FootballField({ yardline100 = 50, ydstogo = 4 }) {
  const offenseYard = 100 - yardline100;
  const firstDownYard = Math.min(100, offenseYard + ydstogo);

  return (
    <div className="football-field" aria-label="Field position visualization">
      <div className="field-endzone field-endzone--own">OWN</div>
      <div className="field-main">
        <div className="field-yard-lines">
          {Array.from({ length: 11 }, (_, i) => (
            <span key={i} className="field-yard-tick" style={{ left: `${i * 10}%` }}>
              {i * 10}
            </span>
          ))}
        </div>
        <div
          className="field-line-of-scrimmage"
          style={{ left: `${offenseYard}%` }}
          title={`${yardline100} yards from opponent end zone`}
        />
        <div
          className="field-first-down"
          style={{ left: `${firstDownYard}%` }}
          title={`${ydstogo} yards to go`}
        />
        <div className="field-ball" style={{ left: `${offenseYard}%` }} />
      </div>
      <div className="field-endzone field-endzone--opp">OPP</div>
      <p className="field-caption">
        {yardline100} yds to score · 4th &amp; {ydstogo}
      </p>
    </div>
  );
}
