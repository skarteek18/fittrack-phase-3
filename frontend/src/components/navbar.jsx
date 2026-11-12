import React from "react";
import { Link, useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    navigate("/login");
  };

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <Link to="/dashboard">
          <h2>FitTrack</h2>
        </Link>
      </div>

      <div className="navbar-links">
        <Link to="/dashboard">Dashboard</Link>
        <Link to="/workouts">Workouts</Link>
        <Link to="/nutrition">Nutrition</Link>
        <Link to="/water">Water Tracker</Link>
        <Link to="/analytics">Analytics</Link>
        <Link to="/reminders">Reminders</Link>
      </div>

      <div className="navbar-actions">
        <button
          className="notification-btn"
          onClick={() => navigate("/notifications")}
          aria-label="Notifications"
        >
          🔔
        </button>

        <button
          className="profile-btn"
          onClick={() => navigate("/profile")}
        >
          👤 Profile
        </button>

        <button
          className="logout-btn"
          onClick={handleLogout}
        >
          Logout
        </button>
      </div>
    </nav>
  );
}

export default Navbar;