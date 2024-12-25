import React, { useState } from "react";
import axios from "axios";
import { useNavigate, useParams } from "react-router-dom";

function Profile() {
  const { id } = useParams(); // Get the user's `id` from the URL
  const [userData, setUserData] = useState({
    age: null,
    profession: null,
    blood_group: null,
    location: null,
  });
  const [formData, setFormData] = useState({
    age: "",
    profession: "",
    blood_group: "",
    location: "",
  });
  const [error, setError] = useState("");
  const [showData, setShowData] = useState(false); // State to toggle data visibility
  const [hasProfileData, setHasProfileData] = useState(false); // Track if the user has profile data
  const navigate = useNavigate();

  const handleShowData = async () => {
    try {
      // Fetch the user's profile data from the backend
      const response = await axios.get(`http://flask-be:5001/fetch-profile?id=${id}`);
      setUserData(response.data); // Set the fetched data to state
      setShowData(!showData); // Toggle data visibility

      // Check if the user has data in all four fields
      if (response.data.age && response.data.profession && response.data.blood_group && response.data.location) {
        setHasProfileData(true);
      }
    } catch (error) {
      console.error("Error fetching profile data:", error);
      setError("Failed to fetch profile data.");
    }
  };

  const handleInsert = async () => {
    const { age, profession, blood_group, location } = formData;

    // Validate that all fields are filled
    if (!age || !profession || !blood_group || !location) {
      setError("All fields (age, profession, blood_group, location) are required.");
      return;
    }

    try {
      // Send profile data to the Flask backend for insertion
      const response = await axios.post("http://flask-be:5001/insert-profile", {
        id,
        age,
        profession,
        blood_group,
        location,
      });
      alert(response.data.message);
      setHasProfileData(true); // Disable "Insert Profile" button after insertion
    } catch (error) {
      console.error("Error inserting profile:", error);
      setError(error.response.data.message || "Failed to insert profile.");
    }
  };

  const handleUpdate = async () => {
    const { age, profession, blood_group, location } = formData;

    // Validate that all fields are filled
    if (!age || !profession || !blood_group || !location) {
      setError("All fields (age, profession, blood_group, location) are required.");
      return;
    }

    try {
      // Send profile data to the Flask backend for updating
      const response = await axios.post("http://flask-be:5001/update-profile", {
        id,
        age,
        profession,
        blood_group,
        location,
      });
      alert(response.data.message);
    } catch (error) {
      console.error("Error updating profile:", error);
      setError(error.response.data.message || "Failed to update profile.");
    }
  };

  const handleLogout = () => {
    navigate("/");
  };

  return (
    <div className="profile-container">
      <h2>Profile</h2>
      {error && <div className="error-message">{error}</div>}
      <div className="profile-details">
        <div className="form-group">
          <label>Age</label>
          <input
            type="number"
            value={formData.age}
            onChange={(e) => setFormData({ ...formData, age: e.target.value })}
          />
        </div>
        <div className="form-group">
          <label>Profession</label>
          <input
            type="text"
            value={formData.profession}
            onChange={(e) => setFormData({ ...formData, profession: e.target.value })}
          />
        </div>
        <div className="form-group">
          <label>Blood Group</label>
          <input
            type="text"
            value={formData.blood_group}
            onChange={(e) => setFormData({ ...formData, blood_group: e.target.value })}
          />
        </div>
        <div className="form-group">
          <label>Location</label>
          <input
            type="text"
            value={formData.location}
            onChange={(e) => setFormData({ ...formData, location: e.target.value })}
          />
        </div>
      </div>
      <div className="button-group">
        <button className="btn" onClick={handleInsert} disabled={hasProfileData}>
          Insert Profile
        </button>
        <button className="btn" onClick={handleUpdate} disabled={!hasProfileData}>
          Update Profile
        </button>
        <button className="btn" onClick={handleShowData}>
          {showData ? "Hide My Data" : "Show My Data"}
        </button>
        <button className="btn" onClick={handleLogout}>
          Logout
        </button>
      </div>

      {/* Display user data when "Show My Data" is clicked */}
      {showData && (
        <div className="user-data">
          <h3>My Profile Data</h3>
          <table>
            <tbody>
              <tr>
                <th>Age</th>
                <td>{userData.age}</td>
              </tr>
              <tr>
                <th>Profession</th>
                <td>{userData.profession}</td>
              </tr>
              <tr>
                <th>Blood Group</th>
                <td>{userData.blood_group}</td>
              </tr>
              <tr>
                <th>Location</th>
                <td>{userData.location}</td>
              </tr>
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Profile;