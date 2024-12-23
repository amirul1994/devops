from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

# Initialize the Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# MySQL connection details
db = mysql.connector.connect(
    host="master-db",
    user="db-user",
    password="Ujh$#9(a^",
    database="bio"
)

# Create a cursor object
cursor = db.cursor()

@app.route('/api/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'GET':
        # Fetch username from the info table
        username_query = "SELECT username FROM info LIMIT 1"
        cursor.execute(username_query)
        username_result = cursor.fetchone()
        username = username_result[0] if username_result else "Unknown User"

        # Fetch profile data from the profile table
        profile_query = "SELECT age, blood_group, location FROM profile"
        cursor.execute(profile_query)
        profile_result = cursor.fetchone()

        if profile_result:
            # Return profile data as JSON
            return jsonify({
                "username": username,
                "age": profile_result[0],
                "blood_group": profile_result[1],
                "location": profile_result[2]
            }), 200
        else:
            return jsonify({"message": "Profile not found"}), 404

    elif request.method == 'POST':
        # Update profile data in the database
        data = request.json
        age = data.get('age')
        blood_group = data.get('blood_group')
        location = data.get('location')

        # Check if a profile already exists
        query = "SELECT * FROM profile"
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            # Update the existing profile
            update_query = "UPDATE profile SET age = %s, blood_group = %s, location = %s"
            cursor.execute(update_query, (age, blood_group, location))
        else:
            # Insert a new profile
            insert_query = "INSERT INTO profile (age, blood_group, location) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (age, blood_group, location))

        db.commit()
        return jsonify({"message": "Profile updated successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)