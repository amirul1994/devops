import React, { useState, useEffect } from 'react';
import axios from 'axios';

function ProfilePage({ username, handleLogout }) {
  const [profileData, setProfileData] = useState({
    username: '',
    age: '',
    blood_group: '',
    location: ''
  });

  // Fetch profile data from the Flask backend
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await axios.get('http://flask-be:5001/api/profile');
        setProfileData(response.data);
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    };

    fetchProfile();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Send profile data to the Flask backend
      const response = await axios.post('http://flask-be:5001/api/profile', {
        age: profileData.age,
        blood_group: profileData.blood_group,
        location: profileData.location
      });

      // Handle success
      console.log(response.data.message);
      alert('Profile updated successfully!');
    } catch (error) {
      // Handle error
      console.error('Error updating profile:', error);
      alert('Error updating profile. Please try again.');
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '400px', margin: '0 auto' }}>
      <h2>Profile</h2>
      <p><strong>Username:</strong> {profileData.username}</p>
      <p><strong>Age:</strong> {profileData.age}</p>
      <p><strong>Blood Group:</strong> {profileData.blood_group}</p>
      <p><strong>Location:</strong> {profileData.location}</p>

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
          <label>
            Age:
            <input
              type="number"
              value={profileData.age}
              onChange={(e) => setProfileData({ ...profileData, age: e.target.value })}
              style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            />
          </label>
        </div>
        <div style={{ marginBottom: '15px' }}>
          <label>
            Blood Group:
            <input
              type="text"
              value={profileData.blood_group}
              onChange={(e) => setProfileData({ ...profileData, blood_group: e.target.value })}
              style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            />
          </label>
        </div>
        <div style={{ marginBottom: '15px' }}>
          <label>
            Location:
            <input
              type="text"
              value={profileData.location}
              onChange={(e) => setProfileData({ ...profileData, location: e.target.value })}
              style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            />
          </label>
        </div>
        <button type="submit" style={{ width: '100%', padding: '10px', backgroundColor: '#007BFF', color: 'white', border: 'none', borderRadius: '5px' }}>
          Update Profile
        </button>
      </form>

      {/* Logout Button */}
      <button onClick={handleLogout} style={{ marginTop: '20px', width: '100%', padding: '10px', backgroundColor: '#dc3545', color: 'white', border: 'none', borderRadius: '5px' }}>
        Logout
      </button>
    </div>
  );
}

export default ProfilePage;