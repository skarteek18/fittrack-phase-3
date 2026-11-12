import React, { useEffect, useState } from "react";
import api from "../api";

function Nutrition() {
  const [meals, setMeals] = useState([]);

  const [summary, setSummary] = useState({
    total_calories: 0,
    total_protein: 0,
    total_carbs: 0,
    total_fats: 0
  });

  const [formData, setFormData] = useState({
    meal_type: "Breakfast",
    food_name: "",
    calories: "",
    protein: "",
    carbs: "",
    fats: ""
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchMeals();
    fetchNutritionSummary();
  }, []);

  // Fetch meals
  const fetchMeals = async () => {
    try {
      const response = await api.get("/nutrition/meals");
      setMeals(response.data);
    } catch (error) {
      setError("Unable to load meals.");
    }
  };

  // Fetch daily nutrition summary
  const fetchNutritionSummary = async () => {
    try {
      const response = await api.get("/nutrition/summary/daily");
      setSummary(response.data);
    } catch (error) {
      console.error("Nutrition summary error:", error);
    }
  };

  // Handle input changes
  const handleChange = (event) => {
    setFormData({
      ...formData,
      [event.target.name]: event.target.value
    });
  };

  // Add meal
  const handleSubmit = async (event) => {
    event.preventDefault();

    setLoading(true);
    setError("");

    try {
      const payload = {
        ...formData,
        calories: Number(formData.calories),
        protein: Number(formData.protein || 0),
        carbs: Number(formData.carbs || 0),
        fats: Number(formData.fats || 0)
      };

      await api.post("/nutrition/meals", payload);

      setFormData({
        meal_type: "Breakfast",
        food_name: "",
        calories: "",
        protein: "",
        carbs: "",
        fats: ""
      });

      await fetchMeals();
      await fetchNutritionSummary();
    } catch (error) {
      setError(
        error.response?.data?.detail || "Failed to add meal."
      );
    } finally {
      setLoading(false);
    }
  };

  // Delete meal
  const deleteMeal = async (mealId) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this meal?"
    );

    if (!confirmed) return;

    try {
      await api.delete(`/nutrition/meals/${mealId}`);

      await fetchMeals();
      await fetchNutritionSummary();
    } catch (error) {
      setError("Unable to delete meal.");
    }
  };

  return (
    <div className="nutrition-container">

      <div className="nutrition-header">
        <div>
          <h1>Nutrition Tracker 🥗</h1>
          <p>Track your daily food intake and nutrition.</p>
        </div>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {/* Nutrition Summary */}

      <div className="nutrition-summary">

        <div className="nutrition-card">
          <h3>Calories</h3>
          <h2>{Number(summary.total_calories || 0).toFixed(0)}</h2>
          <p>kcal consumed</p>
        </div>

        <div className="nutrition-card">
          <h3>Protein</h3>
          <h2>{Number(summary.total_protein || 0).toFixed(1)} g</h2>
          <p>Daily intake</p>
        </div>

        <div className="nutrition-card">
          <h3>Carbs</h3>
          <h2>{Number(summary.total_carbs || 0).toFixed(1)} g</h2>
          <p>Daily intake</p>
        </div>

        <div className="nutrition-card">
          <h3>Fats</h3>
          <h2>{Number(summary.total_fats || 0).toFixed(1)} g</h2>
          <p>Daily intake</p>
        </div>

      </div>

      {/* Add Meal Form */}

      <div className="nutrition-form-section">

        <h2>Add Your Meal</h2>

        <form onSubmit={handleSubmit} className="nutrition-form">

          <div className="form-group">
            <label>Meal Type</label>

            <select
              name="meal_type"
              value={formData.meal_type}
              onChange={handleChange}
            >
              <option value="Breakfast">Breakfast</option>
              <option value="Lunch">Lunch</option>
              <option value="Dinner">Dinner</option>
              <option value="Snacks">Snacks</option>
            </select>
          </div>

          <div className="form-group">
            <label>Food Name</label>

            <input
              type="text"
              name="food_name"
              placeholder="Enter food name"
              value={formData.food_name}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Calories (kcal)</label>

            <input
              type="number"
              name="calories"
              min="0"
              placeholder="Calories"
              value={formData.calories}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Protein (g)</label>

            <input
              type="number"
              name="protein"
              min="0"
              step="0.1"
              placeholder="Protein"
              value={formData.protein}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label>Carbs (g)</label>

            <input
              type="number"
              name="carbs"
              min="0"
              step="0.1"
              placeholder="Carbohydrates"
              value={formData.carbs}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label>Fats (g)</label>

            <input
              type="number"
              name="fats"
              min="0"
              step="0.1"
              placeholder="Fats"
              value={formData.fats}
              onChange={handleChange}
            />
          </div>

          <button
            type="submit"
            className="nutrition-submit-btn"
            disabled={loading}
          >
            {loading ? "Adding..." : "Add Meal"}
          </button>

        </form>
      </div>

      {/* Meal History */}

      <div className="meal-history">

        <h2>Today's Meals</h2>

        {meals.length === 0 ? (
          <p>No meals recorded yet.</p>
        ) : (
          <div className="meal-list">

            {meals.map((meal) => (

              <div className="meal-card" key={meal.id}>

                <div>
                  <h3>{meal.food_name}</h3>
                  <p>{meal.meal_type}</p>
                </div>

                <div className="meal-details">
                  <span>{meal.calories} kcal</span>
                  <span>Protein: {meal.protein}g</span>
                  <span>Carbs: {meal.carbs}g</span>
                  <span>Fats: {meal.fats}g</span>
                </div>

                <button
                  className="delete-meal-btn"
                  onClick={() => deleteMeal(meal.id)}
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

export default Nutrition;