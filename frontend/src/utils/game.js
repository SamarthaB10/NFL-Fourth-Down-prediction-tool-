export function toGameSeconds(minutes, seconds) {
  return (minutes ?? 0) * 60 + (seconds ?? 0);
}

export function fromGameSeconds(total) {
  const minutes = Math.floor(total / 60);
  const seconds = total % 60;
  return { clockMinutes: minutes, clockSeconds: seconds };
}

export function formatClock(minutes, seconds) {
  const m = String(minutes ?? 0).padStart(2, "0");
  const s = String(seconds ?? 0).padStart(2, "0");
  return `${m}:${s}`;
}

export function formatQuarter(qtr) {
  if (qtr === 5) return "OT";
  return `Q${qtr}`;
}

export function scoreDifferential(scoreOff, scoreDef) {
  return (scoreOff ?? 0) - (scoreDef ?? 0);
}

export function formatScoreDiff(diff) {
  if (diff > 0) return `+${diff}`;
  return String(diff);
}
