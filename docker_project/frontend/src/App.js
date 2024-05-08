import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [isLogin, setIsLogin] = useState(true);
  const [userData, setUserData] = useState({
    name: '',
    age: '',
    profession: '',
    address: '', // Added address field
    password: '',
  });
  const [loggedInUser, setLoggedInUser] = useState(null);
  const [searchName, setSearchName] = useState('');
  const [searchResult, setSearchResult] = useState(null);
  const [signupSuccess, setSignupSuccess] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setUserData({ ...userData, [name]: value });
  };

  const handleSwitchForm = () => {
    setIsLogin(!isLogin);
  };

  const handleSignup = async () => {
    try {
      console.log('User Data:', userData);
      // Make a POST request to signup endpoint
      // docker host machine ip address is used to make it 
      // available in the local network
      // otherwise use load balancer container's ip address
      const response = await axios.post('http://192.168.0.10/info/signup/', userData);

      // Check if signup was successful
      if (response.status === 201) {
        alert('Signup successful!')
        console.log('Signup successful!');

        // Extract JWT tokens from the response data
        const accessToken = response.data.access;
        const refreshToken = response.data.refresh;

        // Store the tokens securely (e.g., in localStorage)
        localStorage.setItem('accessToken', accessToken);
        localStorage.setItem('refreshToken', refreshToken);

        // Update state to indicate signup success and switch to login form
        setSignupSuccess(true);
        setIsLogin(true);
      } else {
        console.log('Signup failed.');
      }
    } catch (error) {
      console.error('Error during signup:', error);
    }
  };

  const handleLogin = async () => {
    try {
      const response = await axios.post('http://192.168.0.10/info/login/', userData);
      console.log(response.data);
      setLoggedInUser({
        name: response.data.user.name,
        age: response.data.user.age,
        profession: response.data.user.profession,
        address: response.data.user.address,
      });
    } catch (error) {
      console.error('Error during login:', error);
    }
  };

  const handleSearch = async () => {
    try {
      const response = await axios.get(`http://192.168.0.10/info/search/?name=${searchName}`);
      console.log(response.data);
      if (response.data && response.data.name) { // Check if response.data has a name property
        setSearchResult(response.data);
      } else {
        setSearchResult({ error: 'User not found' }); // Set searchResult with an error message
      }
    } catch (error) {
      console.error('Error during search:', error);
      setSearchResult({ error: 'User not found' }); // Set searchResult with an error message
    }
  };

  return (
    <div className="App">
      <h1>User Authentication</h1>
      {isLogin ? (
        <div>
          <h2>Login</h2>
          <input type="text" placeholder="Username" name="name" onChange={handleInputChange} />
          <input type="password" placeholder="Password" name="password" onChange={handleInputChange} />
          <button onClick={handleLogin}>Login</button>
          <p>Don't have an account? <button onClick={handleSwitchForm}>Sign Up</button></p>
        </div>
      ) : (
        <div>
          <h2>Sign Up</h2>
          <input type="text" placeholder="Name" name="name" onChange={handleInputChange} />
          <input type="text" placeholder="Age" name="age" onChange={handleInputChange} />
          <input type="text" placeholder="Profession" name="profession" onChange={handleInputChange} />
          <input type="text" placeholder="Address" name="address" onChange={handleInputChange} /> {/* Added address field */}
          <input type="password" placeholder="Password" name="password" onChange={handleInputChange} />
          <button onClick={handleSignup}>Sign Up</button>

          <p>Already have an account? <button onClick={handleSwitchForm}>Login</button></p>
        </div>
      )}

      {loggedInUser && (
        <div className="user-details">
          <h2>User Details</h2>
          <p>Name: {loggedInUser.name}</p>
          <p>Age: {loggedInUser.age}</p>
          <p>Profession: {loggedInUser.profession}</p>
          <p>Address: {loggedInUser.address}</p>
        </div>
      )}

      <div>
        <h2>Search User</h2>
        <input type="text" placeholder="Search by name" value={searchName} onChange={(e) => setSearchName(e.target.value)} />
        <button onClick={handleSearch}>Search</button>

        {searchResult && searchResult.error ? (
          <p>{searchResult.error}</p>
        ) : searchResult && (
          <div className="search-result">
            <h3>User Found</h3>
            <p>Name: {searchResult.name}</p>
            <p>Age: {searchResult.age}</p>
            <p>Profession: {searchResult.profession}</p>
            <p>Address: {searchResult.address}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
