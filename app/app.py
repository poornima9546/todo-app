from flask import Flask, request, jsonify
from database import get_connection
import logging


# Create the Flask application
app = Flask(__name__)


# Configure application logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# Home route
@app.route("/")
def home():
    return jsonify({
        "message": "To-Do Application is running"
    })


# Health check route
@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    }), 200


# Get all todos
@app.route("/todos", methods=["GET"])
def get_todos():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM todos ORDER BY id")

    todos = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(todos)


# Create a new todo
@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.get_json()

    title = data.get("title")
    description = data.get("description", "")

    # Check if title was provided
    if not title:
        return jsonify({
            "error": "Title is required"
        }), 400

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO todos (title, description)
        VALUES (%s, %s)
        """,
        (title, description)
    )

    connection.commit()

    todo_id = cursor.lastrowid

    cursor.close()
    connection.close()

    logging.info("Created todo with ID %s", todo_id)

    return jsonify({
        "message": "Todo created",
        "id": todo_id
    }), 201


# Update an existing todo
@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.get_json()

    completed = data.get("completed")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE todos
        SET completed = %s
        WHERE id = %s
        """,
        (completed, todo_id)
    )

    connection.commit()

    cursor.close()
    connection.close()

    logging.info("Updated todo with ID %s", todo_id)

    return jsonify({
        "message": "Todo updated"
    })


# Delete a todo
@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM todos WHERE id = %s",
        (todo_id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    logging.info("Deleted todo with ID %s", todo_id)

    return jsonify({
        "message": "Todo deleted"
    })


# Start the Flask development server
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
