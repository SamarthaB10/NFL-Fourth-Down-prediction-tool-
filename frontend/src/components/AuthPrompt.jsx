import { Link } from "react-router-dom";

export default function AuthPrompt({
  title = "Sign in required",
  description = "Create a free account to run drive simulations and save your session.",
}) {
  return (
    <div className="auth-prompt">
      <div className="auth-prompt-icon" aria-hidden>
        🔒
      </div>
      <h3>{title}</h3>
      <p>{description}</p>
      <div className="auth-prompt-actions">
        <Link to="/login" className="btn-primary btn-primary--inline">
          Sign in
        </Link>
        <Link to="/register" className="btn-retry">
          Create account
        </Link>
      </div>
    </div>
  );
}
