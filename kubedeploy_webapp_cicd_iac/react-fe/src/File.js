import React, { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

function File() {
  const [selectedFile, setSelectedFile] = useState(null); // State to store the selected file
  const [error, setError] = useState(""); // State to handle error messages
  const [success, setSuccess] = useState(""); // State to handle success messages
  const [isUploading, setIsUploading] = useState(false); // State to track upload progress
  const navigate = useNavigate();
  const { id } = useParams(); // Get the `id` from the URL

  // Handle file selection
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Check if the file is a document (e.g., PDF, DOC, TXT)
      const allowedTypes = ["application/pdf", "application/msword", "text/plain"];
      if (allowedTypes.includes(file.type)) {
        setSelectedFile(file);
        setError(""); // Clear any previous error
      } else {
        setSelectedFile(null);
        setError("Only document files (PDF, DOC, TXT) are allowed.");
      }
    } else {
      setSelectedFile(null);
      setError("Please select a file.");
    }
  };

  // Handle file upload confirmation
  const handleUpload = async () => {
    if (!selectedFile) {
      setError("Please select a file to upload.");
      return;
    }

    setIsUploading(true); // Start upload process
    setError(""); // Clear any previous error
    setSuccess(""); // Clear any previous success message

    // Create a FormData object to send the file
    const formData = new FormData();
    formData.append("file", selectedFile); // Append the file to the FormData object

    try {
      // Send the file to the .NET backend
      const response = await fetch("http://dotnet-be:5003/api/upload", {
        method: "POST",
        body: formData, // Send the FormData object
      });

      if (response.ok) {
        const result = await response.json();
        setSuccess("File uploaded successfully!");
        alert("File uploaded successfully!");
      } else {
        throw new Error("Failed to upload file.");
      }
    } catch (error) {
      console.error("Error uploading file:", error);
      setError("Failed to upload file.");
      alert("Failed to upload file.");
    } finally {
      setIsUploading(false); // End upload process
    }
  };

  return (
    <div className="file-container">
      {/* Include CSS directly in the component */}
      <style>
        {`
          .file-container {
            max-width: 500px;
            margin: 0 auto;
            padding: 20px;
            text-align: center;
          }

          .error-message {
            color: red;
            margin-bottom: 10px;
          }

          .success-message {
            color: green;
            margin-bottom: 10px;
          }

          .file-upload-section {
            margin-bottom: 20px;
          }

          .browse-button {
            display: inline-block;
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            cursor: pointer;
            border-radius: 5px;
          }

          .browse-button:hover {
            background-color: #0056b3;
          }

          .selected-file {
            margin-top: 10px;
          }

          .button-group {
            display: flex;
            justify-content: center;
            gap: 10px;
          }

          .btn {
            padding: 10px 20px;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
          }

          .btn:disabled {
            background-color: #cccccc;
            cursor: not-allowed;
          }

          .btn:hover:not(:disabled) {
            background-color: #218838;
          }
        `}
      </style>

      <h2>File Upload</h2>
      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}

      <div className="file-upload-section">
        <input
          type="file"
          id="file-input"
          onChange={handleFileChange}
          style={{ display: "none" }} // Hide the default file input
          accept=".pdf,.doc,.txt" // Restrict file types to PDF, DOC, and TXT
        />
        <label htmlFor="file-input" className="browse-button">
          Browse
        </label>
        {selectedFile && (
          <div className="selected-file">
            <p>Selected File: {selectedFile.name}</p>
          </div>
        )}
      </div>

      <div className="button-group">
        <button
          className="btn"
          onClick={handleUpload}
          disabled={!selectedFile || isUploading}
        >
          {isUploading ? "Uploading..." : "Confirm Upload"}
        </button>
      </div>
    </div>
  );
}

export default File;