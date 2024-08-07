// app.js
const express = require('express');
const app = express();
const PORT = 3000;

// Set EJS as the templating engine
app.set('view engine', 'ejs');

// Middleware to parse URL-encoded data (from forms)
app.use(express.urlencoded({ extended: true }));

// Simple in-memory array to store to-do items
let todoItems = [];

// Route to display the to-do list
app.get('/', (req, res) => {
  res.render('index', { todoItems });
});

// Route to add a new to-do item
app.post('/add', (req, res) => {
  const { newItem } = req.body;
  if (newItem) {
    todoItems.push(newItem);
  }
  res.redirect('/');
});

// Route to delete a to-do item
app.post('/delete', (req, res) => {
  const { index } = req.body;
  if (index !== undefined) {
    todoItems.splice(index, 1);
  }
  res.redirect('/');
});

// Start the server
app.listen(PORT, '0.0.0.0', () => { // Listen on all network interfaces
  console.log(`Server is running on http://0.0.0.0:${PORT}`);
});
