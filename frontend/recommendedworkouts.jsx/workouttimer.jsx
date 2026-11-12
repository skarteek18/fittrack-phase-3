import React, { useEffect, useState } from "react";
import api from "../api";
import "./WorkoutTimer.css";

const WorkoutTimer = () => {
  const [workoutType, setWorkoutType] = useState("running");
  const [activeWorkout, setActiveWorkout] = useState(null);
  const [history, setHistory] = useState([]);
  const [elapsedTime, setElapsedTime] = useState(0);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetchActiveWorkout();
    fetchWorkoutHistory();
  }, []);

  useEffect(() => {
    if (!activeWorkout) return;

    const interval = setInterval(() => {
      const startTime = new Date(activeWorkout.start_time).getTime();
      const currentTime = Date.now();

      setElapsedTime(
        Math.max(0, Math.floor((currentTime - startTime) / 1000))
      );
    }, 1000);

    return () => clearInterval(interval);
  }, [activeWorkout]);

  const fetchActiveWorkout = async () => {
    try {
      const response = await api.get("/workout-timer/active");

      if (response.data) {
        setActiveWorkout(response.data);
      }
    } catch (error) {
      console.error("Failed to fetch active workout:", error);
    }
  };

  const fetchWorkoutHistory = async () => {
    try {
      const response = await api.get("/workout-timer/history");
      setHistory(Array.isArray(response.data) ? response.data : []);
    } catch (error) {
      console.error("Failed to fetch workout history:", error);
    }
  };

  const startWorkout = async () => {
    setLoading(true);
    setMessage("");

    try {
      const response = await api.post("/workout-timer/start", {
        workout_type: workoutType,
      });

      setActiveWorkout(response.data);
      setElapsedTime(0);
      setMessage("Workout started successfully!");
    } catch (error) {
      setMessage(
        error.response?.data?.detail || "Unable to start workout."
      );
    } finally {
      setLoading(false);
    }
  };

  const stopWorkout = async () => {
    if (!activeWorkout) return;

    setLoading(true);
    setMessage("");

    try {
      await api.post(
        `/workout-timer/stop/${activeWorkout.id}`,
        {}
      );

      setActiveWorkout(null);
      setElapsedTime(0);
      setMessage("Workout completed successfully!");

      await fetchWorkoutHistory();
    } catch (error) {
      setMessage(
        error.response?.data?.detail || "Unable to stop workout."
      );
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const remainingSeconds = seconds % 60;

    return [
      hours.toString().padStart(2, "0"),
      minutes.toString().padStart(2, "0"),
      remainingSeconds.toString().padStart(2, "0"),
    ].join(":");
  };

  const formatDate = (dateValue) => {
    if (!dateValue) return "N/A";

    return new Date(dateValue).toLocaleString();
  };

  return (
    <div className="workout-timer-page">
      <div className="timer-header">
        <h1>Workout Timer</h1>
        <p>Track your workout sessions in real time.</p>
      </div>

      {message && (
        <div className="timer-message">
          {message}
        </div>
      )}

      <div className="timer-card">
        <h2>
          {activeWorkout ? "Workout in Progress" : "Ready to Start?"}
        </h2>

        {activeWorkout ? (
          <>
            <div className="timer-display">
              {formatTime(elapsedTime)}
            </div>

            <p className="active-workout-type">
              Current Activity:{" "}
              <strong>{activeWorkout.workout_type}</strong>
            </p>

            <button
              className="stop-workout-button"
              onClick={stopWorkout}
              disabled={loading}
            >
              {loading ? "Please wait..." : "Stop Workout"}
            </button>
          </>
        ) : (
          <>
            <div className="timer-display">00:00:00</div>

            <label htmlFor="workoutType">
              Select Workout Type
            </label>

            <select
              id="workoutType"
              value={workoutType}
              onChange={(event) => setWorkoutType(event.target.value)}
              disabled={loading}
            >
              <option value="running">Running</option>
              <option value="walking">Walking</option>
              <option value="cycling">Cycling</option>
              <option value="weight training">Weight Training</option>
              <option value="yoga">Yoga</option>
              <option value="cardio">Cardio</option>
            </select>

            <button
              className="start-workout-button"
              onClick={startWorkout}
              disabled={loading}
            >
              {loading ? "Starting..." : "Start Workout"}
            </button>
          </>
        )}
      </div>

      <div className="workout-history">
        <h2>Workout History</h2>

        {history.length === 0 ? (
          <p className="empty-history">
            No workout sessions found. Start your first workout!
          </p>
        ) : (
          <div className="history-table-wrapper">
            <table className="history-table">
              <thead>
                <tr>
                  <th>Workout</th>
                  <th>Duration</th>
                  <th>Calories</th>
                  <th>Date</th>
                </tr>
              </thead>

              <tbody>
                {history.map((workout) => (
                  <tr key={workout.id}>
                    <td>{workout.workout_type}</td>
                    <td>{workout.duration ?? 0} min</td>
                    <td>{workout.calories_burned ?? 0} kcal</td>
                    <td>{formatDate(workout.created_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default WorkoutTimer;