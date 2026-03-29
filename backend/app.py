from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from db import get_db_connection

app = Flask(__name__)
CORS(app)

# ================= USER APIs =================

# Register
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
        (data['name'], data['email'], data['password'])
    )
    conn.commit()

    cursor.close()
    conn.close()
    return jsonify({"message": "User registered"})


# Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE email=%s AND password=%s",
        (data['email'], data['password'])
    )
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return jsonify(user)
    return jsonify({"error": "Invalid credentials"}), 401


# Get User Profile
@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, name, email FROM users WHERE id=%s", (id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()
    return jsonify(user)


# ================= TASK APIs =================

# Create Task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks (title, description, status, created_date)
        VALUES (%s, %s, %s, %s)
    """, (data['title'], data.get('description', ''), 'pending', datetime.now()))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Task created"})


# Get Tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tasks ORDER BY created_date DESC")
    tasks = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify(tasks)


# Update Task
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE tasks SET status='completed' WHERE id=%s", (id,))
    conn.commit()

    cursor.close()
    conn.close()
    return jsonify({"message": "Updated"})


# Delete Task
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id=%s", (id,))
    conn.commit()

    cursor.close()
    conn.close()
    return jsonify({"message": "Deleted"})


if __name__ == '__main__':
    app.run(debug=True)