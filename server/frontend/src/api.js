export const API_BASE =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api";

export async function apiRequest(path, { token, ...options } = {}) {
  const headers = new Headers(options.headers || {});
  if (options.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }
  if (token) headers.set("Authorization", `Token ${token}`);

  const response = await fetch(`${API_BASE}${path}`, { ...options, headers });
  const payload = response.status === 204 ? null : await response.json();
  if (!response.ok) {
    const message =
      payload?.detail ||
      payload?.error ||
      Object.values(payload || {}).flat().find((value) => typeof value === "string") ||
      `Request failed (${response.status})`;
    throw new Error(message);
  }
  return payload;
}
