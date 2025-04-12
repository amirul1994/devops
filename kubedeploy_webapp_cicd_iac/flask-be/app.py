from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# MySQL Connection
db = mysql.connector.connect(
    host="mysql-db",  # MySQL host
    user="db-user",  # MySQL user
    password="Ujh$#9(a^",  # MySQL password
    database="bio",  # Database name
    port=3306,  # MySQL port
)

# Insert Profile Data Endpoint
@app.route("/insert-profile", methods=["POST"])
def insert_profile():
    data = request.json
    user_id = data.get("id")  # Get the user's `id`

    # Extract data
    age = data.get("age")
    profession = data.get("profession")
    blood_group = data.get("blood_group")
    location = data.get("location")

    # Validate that all fields are provided
    if not age or not profession or not blood_group or not location:
        return jsonify({"message": "All fields (age, profession, blood_group, location) are required."}), 400

    # Check if the user already has profile data in any of the four fields
    cursor = db.cursor(dictionary=True)
    sql_check = "SELECT age, profession, blood_group, location FROM info WHERE id = %s"
    cursor.execute(sql_check, (user_id,))
    user_data = cursor.fetchone()

    if user_data and (user_data["age"] or user_data["profession"] or user_data["blood_group"] or user_data["location"]):
        # If the user already has data in any of the four fields, return an error
        return jsonify({"message": "User already has profile data. Cannot insert again."}), 400
    else:
        # If the user does not have data in any of the four fields, insert the profile
        sql_insert = """
        UPDATE info
        SET age = %s, profession = %s, blood_group = %s, location = %s
        WHERE id = %s
        """
        values = (age, profession, blood_group, location, user_id)
        cursor.execute(sql_insert, values)
        db.commit()
        return jsonify({"message": "Profile inserted successfully"})

# Update Profile Data Endpoint
@app.route("/update-profile", methods=["POST"])
def update_profile():
    data = request.json
    user_id = data.get("id")  # Get the user's `id`

    # Extract data
    age = data.get("age")
    profession = data.get("profession")
    blood_group = data.get("blood_group")
    location = data.get("location")

    # Validate that all fields are provided
    if not age or not profession or not blood_group or not location:
        return jsonify({"message": "All fields (age, profession, blood_group, location) are required."}), 400

    # Update the profile data
    cursor = db.cursor(dictionary=True)
    sql_update = """
    UPDATE info
    SET age = %s, profession = %s, blood_group = %s, location = %s
    WHERE id = %s
    """
    values = (age, profession, blood_group, location, user_id)
    cursor.execute(sql_update, values)
    db.commit()
    return jsonify({"message": "Profile updated successfully"})

# Fetch Profile Data Endpoint
@app.route("/fetch-profile", methods=["GET"])
def fetch_profile():
    user_id = request.args.get("id")  # Get the user's `id` from the query parameter

    # Fetch the user's profile data
    cursor = db.cursor(dictionary=True)
    sql_fetch = "SELECT age, profession, blood_group, location FROM info WHERE id = %s"
    cursor.execute(sql_fetch, (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        return jsonify(user_data)
    else:
        return jsonify({"message": "No profile data found for this user."}), 404

# Start the Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)  # Run on port 5001