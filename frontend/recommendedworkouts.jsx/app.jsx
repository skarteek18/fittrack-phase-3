import React from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
  Outlet,
} from "react-router-dom";

import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";

import Nutrition from "./components/Nutrition";
import WaterTracker from "./components/WaterTracker";
import WorkoutTimer from "./components/WorkoutTimer";
import Integrations from "./components/Integrations";
import Analytics from "./components/Analytics";
import Reminders from "./components/Reminders";

// Placeholder pages for existing Phase 1 and Phase 2 modules
const Dashboard = () => (
  <div className="page-content">
    <h1>FitTrack Dashboard</h1>
    <p>Welcome to your fitness dashboard!</p>
  </div>
);

const Workouts = () => (
  <div className="page-content">
    <h1>Workouts</h1>
    <p>Manage and track your workouts.</p>
  </div>
);

const WorkoutPlans = () => (
  <div className="page-content">
    <h1>Workout Plans</h1>
    <p>Manage your personalized workout schedules.</p>
  </div>
);

const AIRecommendations = () => (
  <div className="page-content">
    <h1>AI Workout Recommendations</h1>
    <p>Explore personalized workout suggestions.</p>
  </div>
);

const Profile = () => (
  <div className="page-content">
    <h1>My Profile</h1>
    <p>Manage your FitTrack profile.</p>
  </div>
);

const Login = () => (
  <div className="auth-page">
    <h1>FitTrack Login</h1>
    <p>Login component will be added here.</p>
  </div>
);

const Register = () => (
  <div className="auth-page">
    <h1>FitTrack Registration</h1>
    <p>Registration component will be added here.</p>
  </div>
);

// Protect routes using JWT token stored in localStorage
const ProtectedRoute = () => {
  const token = localStorage.getItem("access_token");

  return token ? <Outlet /> : <Navigate to="/login" replace />;
};

// Main application layout
const MainLayout = () => {
  return (
    <>
      <Navbar />

      <div className="app-layout">
        <Sidebar />

        <main className="main-content">
          <Outlet />
        </main>
      </div>
    </>
  );
};

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected Routes */}
        <Route element={<ProtectedRoute />}>
          <Route element={<MainLayout />}>
            <Route
              path="/dashboard"
              element={<Dashboard />}
            />

            <Route
              path="/workouts"
              element={<Workouts />}
            />

            <Route
              path="/workout-plans"
              element={<WorkoutPlans />}
            />

            <Route
              path="/workout-timer"
              element={<WorkoutTimer />}
            />

            <Route
              path="/nutrition"
              element={<Nutrition />}
            />

            <Route
              path="/water"
              element={<WaterTracker />}
            />

            <Route
              path="/recommendations"
              element={<AIRecommendations />}
            />

            <Route
              path="/analytics"
              element={<Analytics />}
            />

            <Route
              path="/integrations"
              element={<Integrations />}
            />

            <Route
              path="/reminders"
              element={<Reminders />}
            />

            <Route
              path="/profile"
              element={<Profile />}
            />
          </Route>
        </Route>

        {/* Default Routes */}
        <Route
          path="/"
          element={<Navigate to="/dashboard" replace />}
        />

        <Route
          path="*"
          element={<Navigate to="/dashboard" replace />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;