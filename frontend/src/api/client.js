// In dev, Vite proxies /api → backend (avoids CORS). Override with VITE_API_URL if needed.
export const API_URL =
  import.meta.env.VITE_API_URL ?? (import.meta.env.DEV ? "/api" : "http://127.0.0.1:8000");

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
  get: async (endpoint) => {
    const response = await fetch(`${API_URL}${endpoint}`, {
      headers: {},
    });
    return parseResponse(response);
  },

  post: async (endpoint, body) => {
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    return parseResponse(response);
  },
};
