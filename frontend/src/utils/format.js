export function formatDecision(name) {
  if (!name) return "N/A";
  return name.replace(/_/g, " ").toUpperCase();
}

export function formatEpa(value) {
  if (value === null || value === undefined) return "N/A";
  const sign = value > 0 ? "+" : "";
  return `${sign}${value}`;
}
