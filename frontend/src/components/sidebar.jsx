import React from "react";
import { NavLink } from "react-router-dom";

function Sidebar() {
  const menuItems = [
    {
      title: "Dashboard",
      path: "/dashboard",
      icon: "📊"
    },
    {
      title: "Workouts",
      path: "/workouts",
      icon: "🏋️"
    },
    {
      title: "Workout Timer",
      path: "/workout-timer",
      icon: "⏱️"
    },
    {
      title: "Workout Plans",
      path: "/workout-plans",
      icon: "📅"
    },
    {
      title: "Nutrition",
      path: "/nutrition",
      icon: "🥗"
    },
    {
      title: "Water Tracker",
      path: "/water",
      icon: "💧"
    },
    {
      title: "AI Recommendations",
      path: "/recommendations",
      icon: "🤖"
    },
    {
      title: "Analytics",
      path: "/analytics",
      icon: "📈"
    },
    {
      title: "Integrations",
      path: "/integrations",
      icon: "🔗"
    },
    {
      title: "Reminders",
      path: "/reminders",
      icon: "🔔"
    },
    {
      title: "Profile",
      path: "/profile",
      icon: "👤"
    }
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2>FitTrack</h2>
        <p>Fitness Management</p>
      </div>

      <nav className="sidebar-menu">
        {menuItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              isActive
                ? "sidebar-link active"
                : "sidebar-link"
            }
          >
            <span className="sidebar-icon">
              {item.icon}
            </span>

            <span>{item.title}</span>
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        <p>FitTrack v3.0</p>
        <span>Stay Healthy 💪</span>
      </div>
    </aside>
  );
}

export default Sidebar;