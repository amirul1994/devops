import React, { useState } from 'react';
import { Link } from 'react-router-dom';

function SignupPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSignup = (e) => {
    e.preventDefault();
    // Handle signup logic here
    console.log('Username:', username);
    console.log('Password:', password);
  };

  return (
    <div style={{ padding: '20px', maxWidth: '400px', margin: '0 auto' }}>
      <h2>Sign Up</h2>
      <form onSubmit={handleSignup}>
        <div style={{ marginBottom: '15px' }}>
          <label>
            Username:
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            />
          </label>
        </div>
        <div style={{ marginBottom: '15px' }}>
          <label>
            Password:
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            />
          </label>
        </div>
        <button type="submit" style={{ width: '100%', padding: '10px', backgroundColor: '#28A745', color: 'white', border: 'none', borderRadius: '5px' }}>
          Sign Up
        </button>
      </form>
      <p style={{ marginTop: '10px', textAlign: 'center' }}>
        Already have an account? <Link to="/">Login</Link>
      </p>
    </div>
  );
}

export default SignupPage;