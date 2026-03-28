from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from db import get_db_connection

app = Flask(__name__)
CORS(app)

# ✅ Create Task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json

    # Validation
    if not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

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

    cursor.close()
    conn.close()

    return jsonify({"message": "Task created successfully"}), 201


# ✅ Get All Tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tasks ORDER BY created_date DESC")
    tasks = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(tasks), 200


# ✅ Update Task Status
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET status = %s WHERE id = %s",
        ("completed", id)
    )
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Task marked as completed"}), 200


# ✅ Delete Task
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Task deleted successfully"}), 200


# ✅ Run Server
if __name__ == '__main__':
    app.run(debug=True)