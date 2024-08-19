from flask import Flask, jsonify
import mysql.connector
from mysql.connector import Error

# Initialize Flask app
app = Flask(__name__)

# Database connection configuration
db_config = {
    'host': 'mysql-container3',
    'user': 'root',
    'password': 'root',
    'database': 'mydb'
}

@app.route('/db_check')
def get_db_connection():
    """Establish and return a database connection."""
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/users')
def get_users():
    """Fetch and return all users from the database."""
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(users)


# Main driver function
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
