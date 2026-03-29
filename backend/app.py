from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from datetime import datetime
from db import get_db_connection
import os

app = Flask(__name__, 
    template_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend'),
    static_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend'),
    static_url_path='')
CORS(app)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/home')
def dashboard():
    return render_template('home.html')

@app.route('/tasks')
def tasks_page():
    return render_template('tasks.html')

@app.route('/add-task')
def add_task_page():
    return render_template('add-task.html')

@app.route('/profile')
def profile_page():
    return render_template('profile.html')

# ================= USER APIs =================

# Register API
@app.route('/api/register', methods=['POST'])
def register_api():
    try:
        data = request.json
        print(f"Register request data: {data}")
        
        if not data or not data.get('name') or not data.get('email') or not data.get('password'):
            return jsonify({"error": "Missing required fields"}), 400
            
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (data['name'], data['email'], data['password'])
        )
        conn.commit()

        cursor.close()
        conn.close()
        return jsonify({"message": "User registered successfully"})
    except Exception as e:
        print(f"Register error: {str(e)}")
        return jsonify({"error": str(e)}), 400


# Login API
@app.route('/api/login', methods=['POST'])
def login_api():
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
@app.route('/api/tasks', methods=['POST'])
def create_task():
    try:
        data = request.json
        print(f"Creating task with data: {data}")
        
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
            
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO tasks (title, description, status, created_date)
            VALUES (%s, %s, %s, %s)
        """, (data['title'], data.get('description', ''), 'pending', datetime.now()))

        conn.commit()
        cursor.close()
        conn.close()

        print("Task created successfully")
        return jsonify({"message": "Task created"})
    except Exception as e:
        print(f"Error creating task: {str(e)}")
        return jsonify({"error": str(e)}), 400


# Get Tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed", "tasks": []}), 500
            
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM tasks ORDER BY created_date DESC")
        tasks = cursor.fetchall()

        cursor.close()
        conn.close()
        
        # Ensure we return a list
        if tasks is None:
            tasks = []
            
        print(f"Retrieved {len(tasks)} tasks from database")
        return jsonify(tasks)
    except Exception as e:
        print(f"Error getting tasks: {str(e)}")
        return jsonify({"error": str(e), "tasks": []}), 500


# Update Task
@app.route('/api/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Get current status
        cursor.execute("SELECT status FROM tasks WHERE id=%s", (id,))
        task = cursor.fetchone()
        
        if not task:
            cursor.close()
            conn.close()
            return jsonify({"error": "Task not found"}), 404

        # Toggle status
        new_status = 'pending' if task['status'] == 'completed' else 'completed'
        
        cursor.execute("UPDATE tasks SET status=%s WHERE id=%s", (new_status, id))
        conn.commit()

        cursor.close()
        conn.close()
        print(f"Task {id} updated to status: {new_status}")
        return jsonify({"message": "Task updated", "status": new_status})
    except Exception as e:
        print(f"Error updating task: {str(e)}")
        return jsonify({"error": str(e)}), 400


# Delete Task
@app.route('/api/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM tasks WHERE id=%s", (id,))
        conn.commit()

        cursor.close()
        conn.close()
        print(f"Task {id} deleted")
        return jsonify({"message": "Deleted"})
    except Exception as e:
        print(f"Error deleting task: {str(e)}")
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)