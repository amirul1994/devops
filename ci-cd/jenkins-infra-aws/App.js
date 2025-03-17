import React, { useState } from 'react';
import Greeting from './Greeting';
import './App.css';

function App() {
  const [name, setName] = useState('');
  const [submittedName, setSubmittedName] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmittedName(name);
  };

  return (
    <div className="App">
      <h1>Simple React App</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter your name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <button type="submit">Greet Me</button>
      </form>
      {submittedName && <Greeting name={submittedName} />}
    </div>
  );
}

export default App;