import { api } from "./client";

export function getHistoricalRecommendation(payload) {
  const body = {
    season: payload.season,
    yardline_100: payload.yardline_100,
    ydstogo: payload.ydstogo,
  };
  if (payload.posteam?.trim()) body.posteam = payload.posteam.trim().toUpperCase();
  if (payload.defteam?.trim()) body.defteam = payload.defteam.trim().toUpperCase();
  return api.post("/recommend", body);
}

export function getMLRecommendation(payload) {
  return api.post("/recommended/ML", {
    yardline_100: payload.yardline_100,
    ydstogo: payload.ydstogo,
    qtr: payload.qtr ?? 4,
    game_seconds_remaining: payload.game_seconds_remaining ?? 900,
    score_differential: payload.score_differential ?? 0,
  });
}

export function getPlays() {
  return api.get("/plays");
}

export function getSeasonSummary(season) {
  return api.get(`/summary/${season}`);
}

export function checkHealth() {
  return api.get("/health");
}
