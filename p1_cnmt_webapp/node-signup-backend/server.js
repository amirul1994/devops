const express = require('express');
const mysql = require('mysql2');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const PORT = 5000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Create a MySQL connection
const db = mysql.createConnection({
  host: 'master-db', // MySQL host
  user: 'db-user',   // MySQL username
  password: 'Ujh$#9(a^', // MySQL password
  database: 'bio'    // MySQL database name
});

// Connect to MySQL
db.connect((err) => {
  if (err) {
    console.error('Error connecting to MySQL:', err);
    return;
  }
  console.log('Connected to MySQL database');
});

// API Endpoint to handle signup
app.post('/api/signup', (req, res) => {
  const { username, password } = req.body;

  // Insert user data into the database
  const sql = 'INSERT INTO info (username, password) VALUES (?, ?)';
  db.query(sql, [username, password], (err, result) => {
    if (err) {
      console.error('Error inserting data:', err);
      return res.status(500).json({ message: 'Error saving user' });
    }
    res.status(201).json({ message: 'User registered successfully' });
  });
});

// Start the server
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Node.js server is running on http://node-be:${PORT}`);
  });