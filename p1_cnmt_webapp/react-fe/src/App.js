import React from "react";
import { BrowserRouter as Router, Route, Routes, Link, useLocation } from "react-router-dom";
import Login from "./Login";
import Signup from "./Signup";
import Profile from "./Profile";
import "./App.css";

function Navbar() {
  const location = useLocation();

  // Hide the navbar on the Profile page
  if (location.pathname.startsWith("/profile")) {
    return null;
  }

  return (
    <nav className="navbar">
      <Link to="/" className="nav-link">
        Login
      </Link>
      <Link to="/signup" className="nav-link">
        Signup
      </Link>
    </nav>
  );
}

function App() {
  return (
    <Router>
      <div className="app">
        <Navbar /> {/* Render the navbar conditionally */}
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/profile/:id" element={<Profile />} /> {/* Pass the `id` to the Profile page */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;