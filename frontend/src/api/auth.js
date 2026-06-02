import { api, setToken } from "./client";

const API_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

export async function register(email, password) {
  return api.post("/auth/register", { email, password });
}

export async function login(email, password) {
  const body = new URLSearchParams();
  body.append("username", email);
  body.append("password", password);
  const response = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });
  const data = await response.json().catch(() => null);
  if (!response.ok) {
    const detail = data?.detail ?? `Login failed (${response.status})`;
    throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
  }
  setToken(data.access_token);
  return data;
}

export function logout() {
  setToken(null);
}

export async function fetchMe() {
  return api.get("/auth/me", { auth: true });
}
