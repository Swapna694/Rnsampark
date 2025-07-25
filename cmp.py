from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
import bcrypt  # Import bcrypt for password hashing

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up MongoDB connection
client = MongoClient('mongodb://localhost:27017/')  # MongoDB connection URL
db = client.rnsampark  # Database name
collection = db.users  # Collection name

# Route to handle registration
@app.route('/register', methods=['POST'])
def register():
    try:
        # Get data from the form
        data = request.get_json()

        # Validate required fields (removed 'pet' from the required fields)
        required_fields = ['name', 'email', 'phone', 'password', 'adhar', 'nickname']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'{field} is required'}), 400

        # Hash the password before storing it
        password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

        # Prepare user data (removed 'pet')
        user_data = {
            'name': data['name'],
            'email': data['email'],
            'phone': data['phone'],
            'password': password_hash,  # Store hashed password
            'adhar': data['adhar'],
            'nickname': data['nickname'],
        }

        # Insert the user data into the collection
        result = collection.insert_one(user_data)

        # Return response
        return jsonify({'message': 'Registration Successful!', 'user_id': str(result.inserted_id)}), 201

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500


# Route to handle login
@app.route('/login', methods=['POST'])
def login():
    try:
        # Get login data (email and password)
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        # Validate input
        if not email or not password:
            return jsonify({'message': 'Email and Password are required'}), 400

        # Find the user by email
        user = collection.find_one({'email': email})

        # Check if user exists
        if not user:
            return jsonify({'message': 'Invalid email or password'}), 401

        # Verify password using bcrypt
        if not bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return jsonify({'message': 'Invalid email or password'}), 401

        # Return success response
        return jsonify({'message': 'Login successful', 'user_id': str(user['_id'])}), 200

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500


# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
