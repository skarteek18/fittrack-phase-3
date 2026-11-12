import React, { useEffect, useState } from "react";
import api from "../api";
import "./Analytics.css";

const Analytics = () => {
  const [weeklyData, setWeeklyData] = useState(null);
  const [monthlyData, setMonthlyData] = useState(null);
  const [goals, setGoals] = useState([]);
  const [consistency, setConsistency] = useState(null);
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    setLoading(true);
    setError("");

    try {
      const [
        weeklyResponse,
        monthlyResponse,
        goalsResponse,
        consistencyResponse,
        insightsResponse,
      ] = await Promise.all([
        api.get("/analytics/weekly"),
        api.get("/analytics/monthly"),
        api.get("/analytics/goals"),
        api.get("/analytics/consistency"),
        api.get("/analytics/insights"),
      ]);

      setWeeklyData(weeklyResponse.data);
      setMonthlyData(monthlyResponse.data);

      setGoals(
        Array.isArray(goalsResponse.data)
          ? goalsResponse.data
          : goalsResponse.data?.goals || []
      );

      setConsistency(consistencyResponse.data);

      const insightData = insightsResponse.data;
      setInsights(
        Array.isArray(insightData)
          ? insightData
          : insightData?.insights || []
      );
    } catch (err) {
      console.error("Analytics loading error:", err);

      setError(
        err.response?.data?.detail ||
          "Unable to load analytics. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const getValue = (data, ...keys) => {
    if (!data) return 0;

    for (const key of keys) {
      if (data[key] !== undefined && data[key] !== null) {
        return data[key];
      }
    }

    return 0;
  };

  const getGoalProgress = (goal) => {
    const target = Number(goal.target_value || 0);
    const current = Number(goal.current_value || 0);

    if (!target) return 0;

    return Math.min(Math.round((current / target) * 100), 100);
  };

  const renderStatCard = (title, value, unit, icon) => (
    <div className="analytics-card" key={title}>
      <div className="analytics-card-icon">{icon}</div>
      <div>
        <p>{title}</p>
        <h2>
          {value} <span>{unit}</span>
        </h2>
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="analytics-page">
        <h2>Loading Analytics...</h2>
      </div>
    );
  }

  return (
    <div className="analytics-page">
      <div className="analytics-header">
        <div>
          <h1>Advanced Analytics</h1>
          <p>Monitor your fitness performance and progress.</p>
        </div>

        <button
          className="analytics-refresh-button"
          onClick={fetchAnalytics}
        >
          Refresh Data
        </button>
      </div>

      {error && (
        <div className="analytics-error">
          {error}
        </div>
      )}

      {/* Weekly Analytics */}
      <section className="analytics-section">
        <h2>Weekly Performance</h2>

        <div className="analytics-grid">
          {renderStatCard(
            "Total Workouts",
            getValue(weeklyData, "total_workouts", "workouts"),
            "",
            "🏋️"
          )}

          {renderStatCard(
            "Workout Duration",
            getValue(weeklyData, "total_duration", "total_minutes"),
            "min",
            "⏱️"
          )}

          {renderStatCard(
            "Calories Burned",
            getValue(weeklyData, "total_calories", "calories_burned"),
            "kcal",
            "🔥"
          )}
        </div>
      </section>

      {/* Monthly Analytics */}
      <section className="analytics-section">
        <h2>Monthly Performance</h2>

        <div className="analytics-grid">
          {renderStatCard(
            "Monthly Workouts",
            getValue(monthlyData, "total_workouts", "workouts"),
            "",
            "📅"
          )}

          {renderStatCard(
            "Total Duration",
            getValue(monthlyData, "total_duration", "total_minutes"),
            "min",
            "⌛"
          )}

          {renderStatCard(
            "Monthly Calories",
            getValue(monthlyData, "total_calories", "calories_burned"),
            "kcal",
            "⚡"
          )}
        </div>
      </section>

      {/* Workout Consistency */}
      <section className="analytics-section">
        <h2>Workout Consistency</h2>

        <div className="consistency-card">
          <div className="consistency-icon">📈</div>

          <div>
            <h3>
              {getValue(
                consistency,
                "consistency_percentage",
                "percentage"
              )}
              %
            </h3>

            <p>Workout consistency</p>
          </div>

          <div className="consistency-details">
            <p>
              Total Active Days:{" "}
              <strong>
                {getValue(consistency, "active_days", "total_active_days")}
              </strong>
            </p>

            <p>
              Current Streak:{" "}
              <strong>
                {getValue(consistency, "current_streak")} days
              </strong>
            </p>
          </div>
        </div>
      </section>

      {/* Goal Progress */}
      <section className="analytics-section">
        <h2>Fitness Goal Progress</h2>

        {goals.length === 0 ? (
          <p className="analytics-empty">No fitness goals available.</p>
        ) : (
          <div className="goal-analytics-grid">
            {goals.map((goal) => {
              const progress = getGoalProgress(goal);

              return (
                <div className="goal-analytics-card" key={goal.id}>
                  <h3>{goal.title || goal.goal_type || "Fitness Goal"}</h3>

                  <div className="goal-progress-info">
                    <span>{progress}%</span>
                    <span>
                      {goal.current_value || 0} / {goal.target_value || 0}
                    </span>
                  </div>

                  <div className="goal-progress-track">
                    <div
                      className="goal-progress-fill"
                      style={{ width: `${progress}%` }}
                    />
                  </div>

                  <p>
                    {progress >= 100
                      ? "Goal completed!"
                      : "Keep working towards your goal."}
                  </p>
                </div>
              );
            })}
          </div>
        )}
      </section>

      {/* Fitness Insights */}
      <section className="analytics-section">
        <h2>Fitness Insights</h2>

        {insights.length === 0 ? (
          <p className="analytics-empty">
            No insights available yet. Continue tracking your workouts!
          </p>
        ) : (
          <div className="insights-list">
            {insights.map((insight, index) => (
              <div className="insight-card" key={index}>
                <span className="insight-icon">💡</span>

                <p>
                  {typeof insight === "string"
                    ? insight
                    : insight.message ||
                      insight.description ||
                      JSON.stringify(insight)}
                </p>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
};

export default Analytics;