import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { apiRequest } from "../../api";
import { useAuth } from "../../auth";

export default function Register() {
  const { signIn } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(event) {
    event.preventDefault();
    setError("");
    setBusy(true);
    const form = new FormData(event.currentTarget);
    const password = form.get("password");
    if (password !== form.get("confirmPassword")) {
      setError("Passwords do not match.");
      setBusy(false);
      return;
    }
    try {
      const user = await apiRequest("/register/", {
        method: "POST",
        body: JSON.stringify({
          username: form.get("username"),
          email: form.get("email"),
          password,
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
        <p className="eyebrow">JOIN OUR COMMUNITY</p>
        <h1>Create your account</h1>
        <p>Save time, share your experience, and find your people.</p>
        <label htmlFor="username">Username</label>
        <input id="username" name="username" autoComplete="username" minLength={3} required />
        <label htmlFor="email">Email</label>
        <input id="email" name="email" type="email" autoComplete="email" required />
        <label htmlFor="password">Password</label>
        <input id="password" name="password" type="password" autoComplete="new-password" minLength={8} required />
        <label htmlFor="confirmPassword">Confirm password</label>
        <input id="confirmPassword" name="confirmPassword" type="password" autoComplete="new-password" required />
        {error && <p className="notice error" role="alert">{error}</p>}
        <button className="button button-full" disabled={busy}>{busy ? "Creating account…" : "Create account"}</button>
        <p className="auth-foot">Already a member? <Link to="/login">Log in</Link></p>
      </form>
    </main>
  );
}
