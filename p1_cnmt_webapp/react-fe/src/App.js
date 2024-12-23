import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import LoginPage from './LoginPage';
import SignupPage from './SignupPage';
import ProfilePage from './ProfilePage';

function App() {
  const [username, setUsername] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate(); // Use useNavigate for redirection

  const handleLogout = () => {
    setUsername(''); // Clear the username
    setIsLoggedIn(false); // Set login status to false
    navigate('/'); // Redirect to the login page
  };

  return (
    <div>
      {isLoggedIn && (
        <button onClick={handleLogout} style={{ margin: '10px', padding: '10px', backgroundColor: '#dc3545', color: 'white', border: 'none', borderRadius: '5px' }}>
          Logout
        </button>
      )}
      <Routes>
        <Route path="/" element={<LoginPage setUsername={setUsername} setIsLoggedIn={setIsLoggedIn} />} />
        <Route path="/signup" element={<SignupPage setUsername={setUsername} setIsLoggedIn={setIsLoggedIn} />} />
        <Route path="/profile" element={<ProfilePage username={username} handleLogout={handleLogout} />} />
      </Routes>
    </div>
  );
}

export default App;