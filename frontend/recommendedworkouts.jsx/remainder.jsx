import React, { useEffect, useState } from "react";
import api from "../api";
import "./Reminders.css";

const Reminders = () => {
  const [reminders, setReminders] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [editingId, setEditingId] = useState(null);

  const initialForm = {
    title: "",
    description: "",
    reminder_type: "workout",
    reminder_time: "",
    is_enabled: true,
  };

  const [form, setForm] = useState(initialForm);

  useEffect(() => {
    fetchReminders();
  }, []);

  const fetchReminders = async () => {
    try {
      const response = await api.get("/reminders/");
      setReminders(
        Array.isArray(response.data) ? response.data : []
      );
    } catch (error) {
      console.error("Failed to fetch reminders:", error);
      setMessage("Unable to load reminders.");
    }
  };

  const handleChange = (event) => {
    const { name, value, type, checked } = event.target;

    setForm((previous) => ({
      ...previous,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const resetForm = () => {
    setForm(initialForm);
    setEditingId(null);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setMessage("");

    try {
      const payload = {
        ...form,
        reminder_time: new Date(form.reminder_time).toISOString(),
      };

      if (editingId) {
        await api.put(`/reminders/${editingId}`, payload);
        setMessage("Reminder updated successfully!");
      } else {
        await api.post("/reminders/", payload);
        setMessage("Reminder created successfully!");
      }

      resetForm();
      await fetchReminders();
    } catch (error) {
      setMessage(
        error.response?.data?.detail || "Unable to save reminder."
      );
    } finally {
      setLoading(false);
    }
  };

  const editReminder = (reminder) => {
    setEditingId(reminder.id);

    setForm({
      title: reminder.title || "",
      description: reminder.description || "",
      reminder_type: reminder.reminder_type || "workout",
      reminder_time: reminder.reminder_time
        ? new Date(reminder.reminder_time)
            .toISOString()
            .slice(0, 16)
        : "",
      is_enabled: reminder.is_enabled ?? true,
    });

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  const toggleReminder = async (reminder) => {
    setLoading(true);
    setMessage("");

    try {
      const action = reminder.is_enabled ? "disable" : "enable";

      await api.patch(`/reminders/${reminder.id}/${action}`);

      setMessage(`Reminder ${action}d successfully!`);
      await fetchReminders();
    } catch (error) {
      setMessage(
        error.response?.data?.detail || "Unable to update reminder."
      );
    } finally {
      setLoading(false);
    }
  };

  const deleteReminder = async (reminderId) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this reminder?"
    );

    if (!confirmed) return;

    setLoading(true);
    setMessage("");

    try {
      await api.delete(`/reminders/${reminderId}`);

      setMessage("Reminder deleted successfully!");
      await fetchReminders();
    } catch (error) {
      setMessage(
        error.response?.data?.detail || "Unable to delete reminder."
      );
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateValue) => {
    if (!dateValue) return "Not scheduled";

    return new Date(dateValue).toLocaleString();
  };

  return (
    <div className="reminders-page">
      <div className="reminders-header">
        <h1>Fitness Reminders</h1>
        <p>Stay consistent with your fitness goals and daily activities.</p>
      </div>

      {message && (
        <div className="reminder-message">
          {message}
        </div>
      )}

      {/* Create / Update Reminder */}
      <div className="reminder-form-card">
        <h2>{editingId ? "Update Reminder" : "Create New Reminder"}</h2>

        <form onSubmit={handleSubmit}>
          <div className="reminder-form-group">
            <label htmlFor="title">Reminder Title</label>
            <input
              id="title"
              type="text"
              name="title"
              placeholder="Enter reminder title"
              value={form.title}
              onChange={handleChange}
              required
            />
          </div>

          <div className="reminder-form-group">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              name="description"
              placeholder="Enter reminder details"
              value={form.description}
              onChange={handleChange}
              rows="3"
            />
          </div>

          <div className="reminder-form-group">
            <label htmlFor="reminder_type">Reminder Type</label>
            <select
              id="reminder_type"
              name="reminder_type"
              value={form.reminder_type}
              onChange={handleChange}
            >
              <option value="workout">Workout</option>
              <option value="nutrition">Nutrition</option>
              <option value="water">Water Intake</option>
              <option value="goal">Fitness Goal</option>
              <option value="general">General</option>
            </select>
          </div>

          <div className="reminder-form-group">
            <label htmlFor="reminder_time">Reminder Date & Time</label>
            <input
              id="reminder_time"
              type="datetime-local"
              name="reminder_time"
              value={form.reminder_time}
              onChange={handleChange}
              required
            />
          </div>

          <label className="reminder-checkbox">
            <input
              type="checkbox"
              name="is_enabled"
              checked={form.is_enabled}
              onChange={handleChange}
            />
            Enable reminder
          </label>

          <div className="reminder-form-actions">
            <button type="submit" disabled={loading}>
              {loading
                ? "Saving..."
                : editingId
                ? "Update Reminder"
                : "Create Reminder"}
            </button>

            {editingId && (
              <button
                type="button"
                className="cancel-button"
                onClick={resetForm}
              >
                Cancel
              </button>
            )}
          </div>
        </form>
      </div>

      {/* Reminder List */}
      <div className="reminder-list-section">
        <h2>My Reminders</h2>

        {reminders.length === 0 ? (
          <p className="empty-reminders">
            No reminders created yet.
          </p>
        ) : (
          <div className="reminder-grid">
            {reminders.map((reminder) => (
              <div className="reminder-card" key={reminder.id}>
                <div className="reminder-card-header">
                  <h3>{reminder.title}</h3>

                  <span
                    className={
                      reminder.is_enabled
                        ? "reminder-active"
                        : "reminder-inactive"
                    }
                  >
                    {reminder.is_enabled ? "Active" : "Disabled"}
                  </span>
                </div>

                <p>{reminder.description || "No description provided."}</p>

               