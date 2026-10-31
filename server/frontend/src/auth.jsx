import { createContext, useContext, useMemo, useState } from "react";

const AuthContext = createContext(null);

function readStoredUser() {
  try {
    return JSON.parse(localStorage.getItem("dealershipUser")) || null;
  } catch {
    return null;
  }
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(readStoredUser);

  function signIn(credentials) {
    localStorage.setItem("dealershipUser", JSON.stringify(credentials));
    setUser(credentials);
  }

  function signOut() {
    localStorage.removeItem("dealershipUser");
    setUser(null);
  }

  const value = useMemo(() => ({ user, signIn, signOut }), [user]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
}
