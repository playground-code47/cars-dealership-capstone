import { useState } from "react";
import { Link, Navigate, Route, Routes, useNavigate } from "react-router-dom";

import { apiRequest } from "./api";
import { useAuth } from "./auth";
import DealerDetail from "./components/DealerDetail.jsx";
import DealerList from "./components/DealerList.jsx";
import Login from "./components/Login.jsx";
import Register from "./components/Register/Register.jsx";

function Navigation() {
  const { user, signOut } = useAuth();
  const navigate = useNavigate();
  const [logoutError, setLogoutError] = useState("");

  async function logout() {
    setLogoutError("");
    try {
      await apiRequest("/logoutuser/", { method: "POST", token: user.token });
    } catch (requestError) {
      setLogoutError(
        `Your browser session was cleared, but server logout failed: ${requestError.message}`,
      );
    } finally {
      signOut();
      navigate("/");
    }
  }

  return (
    <>
    <header className="topbar">
      <Link className="brand" to="/" aria-label="Driveway home">
        <span className="brand-mark">D</span> driveway
      </Link>
      <nav aria-label="Main navigation">
        <a href="/About.html">About</a>
        <a href="/Contact.html">Contact</a>
        {user ? (
          <>
            <span className="welcome">Hi, {user.username}</span>
            <button className="button button-outline button-small" onClick={logout}>
              Log out
            </button>
          </>
        ) : (
          <>
            <Link to="/login">Log in</Link>
            <Link className="button button-small" to="/register">Create account</Link>
          </>
        )}
      </nav>
    </header>
    {logoutError && <p className="notice error logout-notice" role="alert">{logoutError}</p>}
    </>
  );
}

export default function App() {
  return (
    <div className="app-shell">
      <Navigation />
      <Routes>
        <Route path="/" element={<DealerList />} />
        <Route path="/dealers/:dealerId" element={<DealerDetail />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
      <footer className="footer">
        <span>© {new Date().getFullYear()} Driveway</span>
        <span>Find a place you can trust.</span>
      </footer>
    </div>
  );
}
