import { useAuth } from "../hooks/useAuth";
import AuthPrompt from "./AuthPrompt";

export default function ProtectedRoute({ children, promptDescription }) {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="loading-card">
        <div className="spinner" />
        <p>Loading account…</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <AuthPrompt description={promptDescription} />;
  }

  return children;
}
