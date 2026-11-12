 import React, { useEffect, useState } from "react";
import api from "../api";
import "./Integrations.css";

const Integrations = () => {
  const [integrations, setIntegrations] = useState([]);
  const [status, setStatus] = useState({});
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const providers = [
    {
      name: "google_fit",
      title: "Google Fit",
      description: "Connect your Google Fit fitness activity data.",
      icon: "🏃",
    },
    {
      name: "apple_health",
      title: "Apple Health",
      description: "Connect your Apple Health fitness activity data.",
      icon: "❤️",
    },
  ];

  useEffect(() => {
    fetchIntegrations();
    fetchIntegrationStatus();
  }, []);

  const fetchIntegrations = async () => {
    try {
      const response = await api.get("/integrations/");
      setIntegrations(
        Array.isArray(response.data) ? response.data : []
      );
    } catch (error) {
      console.error("Failed to fetch integrations:", error);
    }
  };

  const fetchIntegrationStatus = async () => {
    try {
      const response = await api.get("/integrations/status");
      setStatus(response.data || {});
    } catch (error) {
      console.error("Failed to fetch integration status:", error);
    }
  };

  const isConnected = (provider) => {
    const integration = integrations.find(
      (item) => item.provider === provider
    );

    return integration?.is_connected === true;
  };

  const connectProvider = async (provider) => {
    setLoading(true);
    setMessage("");

    try {
      await api.post("/integrations/connect", {
        provider,
      });

      setMessage(`${provider.replace("_", " ")} connected successfully.`);

      await fetchIntegrations();
      await fetchIntegrationStatus();
    } catch (error) {
      setMessage(
        error.response?.data?.detail || "Unable to connect integration."
      );
    } finally {
      setLoading(false);
    }
  };

  const disconnectProvider = async (provider) => {
    const confirmed = window.confirm(
      `Are you sure you want to disconnect ${provider.replace("_", " ")}?`
    );

    if (!confirmed) return;

    setLoading(true);
    setMessage("");

    try {
      await api.delete(`/integrations/${provider}`);

      setMessage(`${provider.replace("_", " ")} disconnected successfully.`);

      await fetchIntegrations();
      await fetchIntegrationStatus();
    } catch (error) {
      setMessage(
        error.response?.data?.detail || "Unable to disconnect integration."
      );
    } finally {
      setLoading(false);
    }
  };

  const syncActivity = async (provider) => {
    setLoading(true);
    setMessage("");

    try {
      await api.post("/integrations/sync", {
        provider,
        steps: 0,
        calories_burned: 0,
        active_minutes: 0,
      });

      setMessage(`${provider.replace("_", " ")} activity synced successfully.`);

      await fetchIntegrations();
      await fetchIntegrationStatus();
    } catch (error) {
      setMessage(
        error.response?.data?.detail || "Activity synchronization failed."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="integrations-page">
      <div className="integrations-header">
        <h1>Fitness Integrations</h1>
        <p>
          Connect external fitness platforms to manage your activity data.
        </p>
      </div>

      {message && (
        <div className="integration-message">
          {message}
        </div>
      )}

      <div className="integration-info">
        <h3>Connected Services</h3>
        <p>
          Manage your external fitness services and synchronize activity
          information with FitTrack.
        </p>
      </div>

      <div className="integration-grid">
        {providers.map((provider) => {
          const connected = isConnected(provider.name);

          return (
            <div className="integration-card" key={provider.name}>
              <div className="integration-icon">
                {provider.icon}
              </div>

              <h2>{provider.title}</h2>

              <p>{provider.description}</p>

              <div
                className={`integration-status ${
                  connected ? "connected" : "disconnected"
                }`}
              >
                {connected ? "Connected" : "Not Connected"}
              </div>

              {connected ? (
                <div className="integration-actions">
                  <button
                    className="sync-button"
                    onClick={() => syncActivity(provider.name)}
                    disabled={loading}
                  >
                    Sync Activity
                  </button>

                  <button
                    className="disconnect-button"
                    onClick={() => disconnectProvider(provider.name)}
                    disabled={loading}
                  >
                    Disconnect
                  </button>
                </div>
              ) : (
                <button
                  className="connect-button"
                  onClick={() => connectProvider(provider.name)}
                  disabled={loading}
                >
                  {loading ? "Please wait..." : "Connect"}
                </button>
              )}
            </div>
          );
        })}
      </div>

      <div className="integration-history">
        <h2>Integration Details</h2>

        {integrations.length === 0 ? (
          <p>No integrations available.</p>
        ) : (
          <div className="integration-table-wrapper">
            <table className="integration-table">
              <thead>
                <tr>
                  <th>Provider</th>
                  <th>Status</th>
                  <th>Connected At</th>
                  <th>Last Synced</th>
                </tr>
              </thead>

              <tbody>
                {integrations.map((item) => (
                  <tr key={item.id}>
                    <td>{item.provider}</td>
                    <td>
                      <span
                        className={
                          item.is_connected
                            ? "table-connected"
                            : "table-disconnected"
                        }
                      >
                        {item.is_connected ? "Connected" : "Disconnected"}
                      </span>
                    </td>
                    <td>
                      {item.connected_at
                        ? new Date(item.connected_at).toLocaleString()
                        : "N/A"}
                    </td>
                    <td>
                      {item.last_synced_at
                        ? new Date(item.last_synced_at).toLocaleString()
                        : "Never"}
                    </td>
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

export default Integrations;