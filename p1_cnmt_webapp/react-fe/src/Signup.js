import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Signup() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate(); // For navigation

  const handleSignup = async (e) => {
    e.preventDefault();

    // Validate that both username and password are provided
    if (!username || !password) {
      setError("Username and password are required.");
      return;
    }

    try {
      // Send signup request to the Node.js backend
      const response = await axios.post("http://node-be:5000/signup", {
        username,
        password,
      });

      // If signup is successful, navigate to the login page
      if (response.data.success) {
        alert("Signup successful! Please log in.");
        navigate("/"); // Redirect to the login page
      } else {
        setError(response.data.message || "Signup failed. Please try again.");
      }
    } catch (error) {
      console.error("Error during signup:", error);
      setError("Signup failed. Please try again.");
    }
  };

  return (
    <div className="form-container">
      <h2>Signup</h2>
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleSignup}>
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
          Signup
        </button>
      </form>
    </div>
  );
}

export default Signup;