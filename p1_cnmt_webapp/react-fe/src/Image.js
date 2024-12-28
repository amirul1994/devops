import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";

const ImageUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [error, setError] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [imagePreview, setImagePreview] = useState(null);
  const navigate = useNavigate();
  const { id } = useParams(); // Get the `id` from the URL

  // Check if the user is logged in (i.e., `id` exists)
  useEffect(() => {
    if (!id) {
      navigate("/"); // Redirect to the login page if `id` is missing
    }
  }, [id, navigate]);

  // Handle file selection
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      // Check if the file is an image
      const allowedExtensions = /(\.jpg|\.jpeg|\.png|\.gif)$/i;
      if (!allowedExtensions.exec(file.name)) {
        setError("Please select a valid image file (JPEG, PNG, GIF).");
        setSelectedFile(null);
        setImagePreview(null);
      } else {
        setError("");
        setSelectedFile(file);
        // Generate image preview
        const reader = new FileReader();
        reader.onloadend = () => {
          setImagePreview(reader.result);
        };
        reader.readAsDataURL(file);
      }
    }
  };

  // Handle image upload
  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select an image file first.");
      return;
    }

    const formData = new FormData();
    formData.append("image", selectedFile);

    setIsUploading(true);
    setUploadStatus("Uploading...");

    try {
      const response = await fetch("http://springboot-be:5002/api/upload-image", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        alert("Image uploaded successfully!");
        setUploadStatus("Image upload successful!");
      } else {
        throw new Error("Image upload failed");
      }
    } catch (error) {
      console.error("Error uploading image:", error);
      alert("Failed to upload image.");
      setUploadStatus("Image upload failed.");
    } finally {
      setIsUploading(false);
    }
  };

  // Handle image update
  const handleUpdate = async () => {
    if (!selectedFile) {
      alert("Please select an image file first.");
      return;
    }

    const formData = new FormData();
    formData.append("image", selectedFile);

    setIsUploading(true);
    setUploadStatus("Updating...");

    try {
      const response = await fetch("http://springboot-be:5002/api/update-image", {
        method: "PUT",
        body: formData,
      });

      if (response.ok) {
        alert("Image updated successfully!");
        setUploadStatus("Image update successful!");
      } else {
        throw new Error("Image update failed");
      }
    } catch (error) {
      console.error("Error updating image:", error);
      alert("Failed to update image.");
      setUploadStatus("Image update failed.");
    } finally {
      setIsUploading(false);
    }
  };

  // Inline styles
  const styles = {
    uploadContainer: {
      backgroundColor: "#fff",
      padding: "20px",
      borderRadius: "8px",
      boxShadow: "0 0 10px rgba(0, 0, 0, 0.1)",
      textAlign: "center",
      width: "300px",
      margin: "50px auto",
    },
    heading: {
      marginBottom: "20px",
      color: "#333",
    },
    browseButton: {
      display: "inline-block",
      padding: "10px 20px",
      backgroundColor: "#007bff",
      color: "white",
      borderRadius: "5px",
      cursor: "pointer",
      marginBottom: "10px",
      transition: "background-color 0.3s ease",
    },
    browseButtonHover: {
      backgroundColor: "#0056b3",
    },
    selectedFile: {
      marginBottom: "20px",
      fontSize: "14px",
      color: "#555",
    },
    confirmButton: {
      padding: "10px 20px",
      backgroundColor: "#28a745",
      color: "white",
      border: "none",
      borderRadius: "5px",
      cursor: "pointer",
      transition: "background-color 0.3s ease",
      marginRight: "10px", // Added margin for spacing
    },
    confirmButtonHover: {
      backgroundColor: "#218838",
    },
    updateButton: {
      padding: "10px 20px",
      backgroundColor: "#ffc107",
      color: "black",
      border: "none",
      borderRadius: "5px",
      cursor: "pointer",
      transition: "background-color 0.3s ease",
    },
    updateButtonHover: {
      backgroundColor: "#e0a800",
    },
    uploadStatus: {
      marginTop: "20px",
      fontSize: "14px",
      color: "#333",
    },
    errorMessage: {
      color: "red",
      marginBottom: "10px",
    },
    imagePreview: {
      maxWidth: "100%",
      maxHeight: "200px",
      marginBottom: "20px",
      borderRadius: "5px",
    },
    loadingSpinner: {
      border: "4px solid #f3f3f3",
      borderTop: "4px solid #3498db",
      borderRadius: "50%",
      width: "30px",
      height: "30px",
      animation: "spin 1s linear infinite",
      margin: "20px auto",
    },
  };

  return (
    <div style={styles.uploadContainer}>
      <h2 style={styles.heading}>Image Upload</h2>
      <div className="upload-section">
        <input
          type="file"
          accept="image/*"
          id="image-input"
          style={{ display: "none" }}
          onChange={handleFileChange}
        />
        <label
          htmlFor="image-input"
          style={styles.browseButton}
          onMouseOver={(e) => (e.target.style.backgroundColor = "#0056b3")}
          onMouseOut={(e) => (e.target.style.backgroundColor = "#007bff")}
        >
          Browse Image
        </label>
        {selectedFile && (
          <p style={styles.selectedFile}>Selected file: {selectedFile.name}</p>
        )}
        {error && <p style={styles.errorMessage}>{error}</p>}
        {imagePreview && (
          <img
            src={imagePreview}
            alt="Preview"
            style={styles.imagePreview}
          />
        )}
        <button
          style={styles.confirmButton}
          onClick={handleUpload}
          onMouseOver={(e) => (e.target.style.backgroundColor = "#218838")}
          onMouseOut={(e) => (e.target.style.backgroundColor = "#28a745")}
          disabled={isUploading}
        >
          {isUploading ? "Uploading..." : "Upload Image"}
        </button>
        <button
          style={styles.updateButton}
          onClick={handleUpdate}
          onMouseOver={(e) => (e.target.style.backgroundColor = "#e0a800")}
          onMouseOut={(e) => (e.target.style.backgroundColor = "#ffc107")}
          disabled={isUploading}
        >
          {isUploading ? "Updating..." : "Update Image"}
        </button>
        {isUploading && <div style={styles.loadingSpinner}></div>}
      </div>
      {uploadStatus && <p style={styles.uploadStatus}>{uploadStatus}</p>}
    </div>
  );
};

export default ImageUpload;