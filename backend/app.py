from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from db import get_db_connection

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return "Task Manager API is running 🚀"

# ✅ Create Task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json

    if not data or not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor()

    try:
        query = """
            INSERT INTO tasks (title, description, status, created_date)
            VALUES (%s, %s, %s, %s)
        """
        values = (
            data["title"],
            data.get("description", ""),
            "pending",
            datetime.now()
        )

        cursor.execute(query, values)
        conn.commit()

        return jsonify({"message": "Task created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# ✅ Get All Tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM tasks ORDER BY created_date DESC")
        tasks = cursor.fetchall()
        return jsonify(tasks), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# ✅ Update Task Status
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor()

    try:
        # Check if task exists
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (id,))
        task = cursor.fetchone()

        if not task:
            return jsonify({"error": "Task not found"}), 404

        cursor.execute(
            "UPDATE tasks SET status = %s WHERE id = %s",
            ("completed", id)
        )
        conn.commit()

        return jsonify({"message": "Task marked as completed"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# ✅ Delete Task
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor()

    try:
        # Check if task exists
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (id,))
        task = cursor.fetchone()

        if not task:
            return jsonify({"error": "Task not found"}), 404

        cursor.execute("DELETE FROM tasks WHERE id = %s", (id,))
        conn.commit()

        return jsonify({"message": "Task deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# ✅ Run Server
if __name__ == '__main__':
    app.run(debug=True)