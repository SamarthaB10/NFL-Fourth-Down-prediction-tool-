import { useCallback, useEffect, useMemo, useState } from "react";
import { fetchMe, login as apiLogin, logout as apiLogout, register as apiRegister } from "../api/auth";
import { getToken } from "../api/client";
import { AuthContext } from "./authContext";

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const refreshUser = useCallback(async () => {
    if (!getToken()) {
      setUser(null);
      setLoading(false);
      return;
    }
    try {
      const me = await fetchMe();
      setUser(me);
    } catch {
      apiLogout();
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    let active = true;
    (async () => {
      if (!getToken()) {
        if (active) {
          setUser(null);
          setLoading(false);
        }
        return;
      }
      try {
        const me = await fetchMe();
        if (active) setUser(me);
      } catch {
        apiLogout();
        if (active) setUser(null);
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => {
      active = false;
    };
  }, []);

  const login = useCallback(
    async (email, password) => {
      await apiLogin(email, password);
      setLoading(true);
      await refreshUser();
    },
    [refreshUser]
  );

  const register = useCallback(
    async (email, password) => {
      await apiRegister(email, password);
      await apiLogin(email, password);
      setLoading(true);
      await refreshUser();
    },
    [refreshUser]
  );

  const logout = useCallback(() => {
    apiLogout();
    setUser(null);
  }, []);

  const value = useMemo(
    () => ({ user, loading, login, register, logout, isAuthenticated: !!user }),
    [user, loading, login, register, logout]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
