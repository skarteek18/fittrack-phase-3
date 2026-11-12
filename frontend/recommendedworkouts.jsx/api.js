import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 15000,
});

// Attach JWT token to every request
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle API errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      if (error.response.status === 401) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("user");

        // Redirect to login if the user is not already there
        if (window.location.pathname !== "/login") {
          window.location.href = "/login";
        }
      }
    } else if (error.request) {
      console.error("Backend server is not responding.");
    } else {
      console.error("API request error:", error.message);
    }

    return Promise.reject(error);
  }
);

export default api;