const express = require("express");
const mysql = require("mysql");
const bodyParser = require("body-parser");
const cors = require("cors");

const app = express();
const port = 5000;

// Middleware
app.use(bodyParser.json());
app.use(cors());

// MySQL Connection
const db = mysql.createConnection({
  host: "mysql-db", // MySQL host
  user: "db-user", // MySQL user
  password: "Ujh$#9(a^", // MySQL password
  database: "bio", // Database name
  port: 3306, // MySQL port
});

// Connect to MySQL
db.connect((err) => {
  if (err) {
    console.error("Error connecting to MySQL:", err);
    return;
  }
  console.log("Connected to MySQL database");
});

// Signup Endpoint
app.post("/signup", (req, res) => {
  const { username, password } = req.body;

  // Validate input
  if (!username || !password) {
    return res.status(400).json({ success: false, message: "Username and password are required." });
  }

  // Check if the user already exists
  const checkUserSql = "SELECT id FROM info WHERE name = ?";
  db.query(checkUserSql, [username], (err, results) => {
    if (err) {
      console.error("Error checking user:", err);
      return res.status(500).json({ success: false, message: "Signup failed" });
    }

    if (results.length > 0) {
      return res.status(409).json({ success: false, message: "Username already exists" });
    }

    // Insert new user into the database
    const insertUserSql = "INSERT INTO info (name, password) VALUES (?, ?)";
    db.query(insertUserSql, [username, password], (err, results) => {
      if (err) {
        console.error("Error inserting user:", err);
        return res.status(500).json({ success: false, message: "Signup failed" });
      }

      return res.status(201).json({ success: true, message: "Signup successful" });
    });
  });
});

// Login Endpoint
app.post("/login", (req, res) => {
  const { username, password } = req.body;

  // Check if the user exists
  const sql = "SELECT id FROM info WHERE name = ? AND password = ?";
  db.query(sql, [username, password], (err, results) => {
    if (err) {
      console.error("Error during login:", err);
      return res.status(500).json({ success: false, message: "Login failed" });
    }

    if (results.length > 0) {
      // Return the user's `id` along with the success message
      return res.status(200).json({ success: true, message: "Login successful", id: results[0].id });
    } else {
      return res.status(401).json({ success: false, message: "Invalid credentials" });
    }
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://node-be:${port}`);
});