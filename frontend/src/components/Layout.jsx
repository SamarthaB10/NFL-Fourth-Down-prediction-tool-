import { useEffect, useState } from "react";
import { NavLink, Outlet } from "react-router-dom";
import { checkHealth } from "../api/recommendations";

const NAV = [
  { to: "/", label: "Home", end: true },
  { to: "/tool", label: "Decision tool" },
  { to: "/plays", label: "Plays" },
  { to: "/dashboard", label: "Dashboard" },
];

export default function Layout() {
  const [backendStatus, setBackendStatus] = useState("connecting");

  useEffect(() => {
    let cancelled = false;
    checkHealth()
      .then(() => {
        if (!cancelled) setBackendStatus("online");
      })
      .catch(() => {
        if (!cancelled) setBackendStatus("offline");
      });
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="app-brand">
          <NavLink to="/" className="app-title-link">
            <h1 className="app-title">
              NFL <span className="highlight">4D</span>
            </h1>
          </NavLink>
          <nav className="app-nav">
            {NAV.map(({ to, label, end }) => (
              <NavLink
                key={to}
                to={to}
                end={end}
                className={({ isActive }) =>
                  `nav-link${isActive ? " nav-link--active" : ""}`
                }
              >
                {label}
              </NavLink>
            ))}
          </nav>
        </div>
        <div className={`status-badge ${backendStatus}`}>
          <span className="status-dot" />
          {backendStatus === "connecting" && "Connecting…"}
          {backendStatus === "online" && "API online"}
          {backendStatus === "offline" && "API offline"}
        </div>
      </header>

      <Outlet />
    </div>
  );
}
