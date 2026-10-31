import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { apiRequest } from "../api";
import { useAuth } from "../auth";

export default function Login() {
  const { signIn } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(event) {
    event.preventDefault();
    setError("");
    setBusy(true);
    const form = new FormData(event.currentTarget);
    try {
      const user = await apiRequest("/loginuser/", {
        method: "POST",
        body: JSON.stringify({
          username: form.get("username"),
          password: form.get("password"),
        }),
      });
      signIn(user);
      navigate("/");
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="auth-page">
      <form className="auth-card" onSubmit={submit}>
        <p className="eyebrow">WELCOME BACK</p>
        <h1>Log in to Driveway</h1>
        <p>Pick up where your next great drive begins.</p>
        <label htmlFor="username">Username</label>
        <input id="username" name="username" autoComplete="username" required />
        <label htmlFor="password">Password</label>
        <input id="password" name="password" type="password" autoComplete="current-password" required />
        {error && <p className="notice error" role="alert">{error}</p>}
        <button className="button button-full" disabled={busy}>{busy ? "Logging in…" : "Log in"}</button>
        <p className="auth-foot">New here? <Link to="/register">Create an account</Link></p>
      </form>
    </main>
  );
}
