// In dev, Vite proxies /api → backend (avoids CORS). Override with VITE_API_URL if needed.
const API_URL =
  import.meta.env.VITE_API_URL ?? (import.meta.env.DEV ? "/api" : "http://127.0.0.1:8000");
const TOKEN_KEY = "nfl4d_token";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
  if (token) localStorage.setItem(TOKEN_KEY, token);
  else localStorage.removeItem(TOKEN_KEY);
}

function authHeaders(extra = {}, useAuth = false) {
  const headers = { ...extra };
  if (useAuth) {
    const token = getToken();
    if (token) headers.Authorization = `Bearer ${token}`;
  }
  return headers;
}

async function parseResponse(response) {
  const data = await response.json().catch(() => null);
  if (!response.ok) {
    const detail =
      data?.detail?.[0]?.msg ??
      data?.detail ??
      data?.message ??
      `Request failed (${response.status})`;
    throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
  }
  return data;
}

export const api = {
  get: async (endpoint, { auth = false } = {}) => {
    const response = await fetch(`${API_URL}${endpoint}`, {
      headers: auth ? authHeaders() : {},
    });
    return parseResponse(response);
  },

  post: async (endpoint, body, { auth = false } = {}) => {
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: "POST",
      headers: authHeaders({ "Content-Type": "application/json" }, auth),
      body: JSON.stringify(body),
    });
    return parseResponse(response);
  },
};
