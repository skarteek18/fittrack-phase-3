import React, { useEffect, useState } from "react";
import api from "../api";

function WaterTracker() {
  const [waterAmount, setWaterAmount] = useState("");
  const [waterGoal, setWaterGoal] = useState(2500);

  const [summary, setSummary] = useState({
    total_intake: 0,
    daily_goal: 2500,
    remaining: 2500,
    completion_percentage: 0,
    goal_completed: false
  });

  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchWaterSummary();
    fetchWaterHistory();
  }, []);

  // Fetch daily water summary
  const fetchWaterSummary = async () => {
    try {
      const response = await api.get("/water/summary");

      setSummary(response.data);
      setWaterGoal(response.data.daily_goal);
    } catch (error) {
      setError("Unable to load water summary.");
    }
  };

  // Fetch water history
  const fetchWaterHistory = async () => {
    try {
      const response = await api.get("/water/history");

      setHistory(response.data);
    } catch (error) {
      setError("Unable to load water history.");
    }
  };

  // Log water intake
  const handleAddWater = async (event) => {
    event.preventDefault();

    if (!waterAmount || Number(waterAmount) <= 0) {
      setError("Please enter a valid water quantity.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      await api.post("/water/log", {
        quantity: Number(waterAmount)
      });

      setWaterAmount("");

      await fetchWaterSummary();
      await fetchWaterHistory();
    } catch (error) {
      setError(
        error.response?.data?.detail || "Failed to log water intake."
      );
    } finally {
      setLoading(false);
    }
  };

  // Update daily water goal
  const handleUpdateGoal = async () => {
    if (!waterGoal || Number(waterGoal) <= 0) {
      setError("Please enter a valid daily water goal.");
      return;
    }

    try {
      await api.post("/water/goal", {
        daily_goal: Number(waterGoal)
      });

      await fetchWaterSummary();

      setError("");
      alert("Water goal updated successfully!");
    } catch (error) {
      setError(
        error.response?.data?.detail || "Unable to update water goal."
      );
    }
  };

  // Delete water record
  const handleDelete = async (recordId) => {
    if (!window.confirm("Delete this water record?")) {
      return;
    }

    try {
      await api.delete(`/water/${recordId}`);

      await fetchWaterSummary();
      await fetchWaterHistory();
    } catch (error) {
      setError("Unable to delete water record.");
    }
  };

  // Quick add water
  const quickAdd = (amount) => {
    setWaterAmount(String(amount));
  };

  const percentage = Math.min(
    Number(summary.completion_percentage || 0),
    100
  );

  return (
    <div className="water-container">

      {/* Header */}

      <div className="water-header">
        <div>
          <h1>Water Tracker 💧</h1>
          <p>Stay hydrated and maintain your daily water goal.</p>
        </div>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {/* Water Summary */}

      <div className="water-summary">

        <div className="water-card">
          <h3>Today's Intake</h3>
          <h2>{summary.total_intake} ml</h2>
          <p>Water consumed</p>
        </div>

        <div className="water-card">
          <h3>Daily Goal</h3>
          <h2>{summary.daily_goal} ml</h2>
          <p>Target intake</p>
        </div>

        <div className="water-card">
          <h3>Remaining</h3>
          <h2>{summary.remaining} ml</h2>
          <p>Water left to drink</p>
        </div>

      </div>

      {/* Progress */}

      <div className="water-progress-section">

        <h2>Daily Hydration Progress</h2>

        <div className="progress-info">
          <span>Goal Progress</span>
          <strong>{percentage}%</strong>
        </div>

        <div className="water-progress-bar">
          <div
            className="water-progress-fill"
            style={{ width: `${percentage}%` }}
          />
        </div>

        <p>
          {summary.goal_completed
            ? "🎉 Congratulations! You reached your daily water goal."
            : `You need ${summary.remaining} ml more to reach your goal.`}
        </p>

      </div>

      {/* Add Water */}

      <div className="water-form-section">

        <h2>Log Water Intake</h2>

        <form onSubmit={handleAddWater}>

          <div className="form-group">
            <label>Water Quantity (ml)</label>

            <input
              type="number"
              min="1"
              placeholder="Enter quantity in ml"
              value={waterAmount}
              onChange={(event) => setWaterAmount(event.target.value)}
              required
            />
          </div>

          <div className="quick-add-buttons">
            <button type="button" onClick={() => quickAdd(150)}>
              +150 ml
            </button>

            <button type="button" onClick={() => quickAdd(250)}>
              +250 ml
            </button>

            <button type="button" onClick={() => quickAdd(500)}>
              +500 ml
            </button>

            <button type="button" onClick={() => quickAdd(750)}>
              +750 ml
            </button>
          </div>

          <button
            type="submit"
            className="water-submit-btn"
            disabled={loading}
          >
            {loading ? "Saving..." : "Add Water"}
          </button>

        </form>

      </div>

      {/* Update Goal */}

      <div className="water-goal-section">

        <h2>Set Daily Water Goal</h2>

        <div className="goal-input-group">

          <input
            type="number"
            min="1"
            value={waterGoal}
            onChange={(event) => setWaterGoal(event.target.value)}
            placeholder="Enter daily goal in ml"
          />

          <button onClick={handleUpdateGoal}>
            Update Goal
          </button>

        </div>

      </div>

      {/* Water History */}

      <div className="water-history">

        <h2>Water Intake History</h2>

        {history.length === 0 ? (
          <p>No water intake records available.</p>
        ) : (
          <div className="water-history-list">

            {history.map((record) => (

              <div className="water-history-card" key={record.id}>

                <div>
                  <h3>💧 {record.quantity} ml</h3>
                  <p>
                    {new Date(record.date).toLocaleDateString()}
                  </p>
                </div>

                <button
                  className="delete-water-btn"
                  onClick={() => handleDelete(record.id)}
                >
                  Delete
                </button>

              </div>

            ))}

          </div>
        )}

      </div>

    </div>
  );
}

export default WaterTracker;