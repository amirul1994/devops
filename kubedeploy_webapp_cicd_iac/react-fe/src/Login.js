import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate(); // For navigation

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      // Send login request to the Node.js backend
      const response = await axios.post("http://node-be:5000/login", {
        username,
        password,
      });

      // If login is successful, navigate to the profile page with the user's `id`
      if (response.data.success) {
        alert("Login successful!");
        navigate(`/profile/${response.data.id}`); // Pass the user's `id` to the profile page
      } else {
        setError(response.data.message || "Invalid credentials. Please try again.");
      }
    } catch (error) {
      console.error("Error during login:", error);
      setError("Login failed. Please try again.");
    }
  };

  return (
    <div className="form-container">
      <h2>Login</h2>
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleLogin}>
        <div className="form-group">
          <label>Username</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn">
          Login
        </button>
      </form>
    </div>
  );
}

export default Login;