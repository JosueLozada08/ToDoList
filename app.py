from flask import Flask, jsonify, request
from flasgger import Swagger
import uuid
from datetime import datetime

app = Flask(__name__)
swagger = Swagger(app)  # Inicializamos Flasgger

# Simulamos una base de datos
tasks = []

@app.route("/")
def home():
    return "Welcome to the ToDoList API!"

@app.route("/tasks", methods=["POST"])
def create_task():
    """
    Crear una nueva tarea
    ---
    tags:
      - Tasks
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              example: "Task 1"
            description:
              type: string
              example: "Description 1"
    responses:
      201:
        description: Tarea creada exitosamente
    """
    data = request.get_json()
    if not data.get("title") or not data.get("description"):
        return jsonify({"error": "Title and description are required"}), 400
    
    task = {
        "id": str(uuid.uuid4()),
        "title": data["title"],
        "description": data["description"],
        "created_at": datetime.now().isoformat(),
        "status": "pending"
    }
    tasks.append(task)
    return jsonify(task), 201

@app.route("/tasks", methods=["GET"])
def list_tasks():
    """
    Listar todas las tareas
    ---
    tags:
      - Tasks
    responses:
      200:
        description: Lista de tareas
    """
    return jsonify(tasks), 200

@app.route("/tasks/<task_id>", methods=["PATCH"])
def update_task(task_id):
    """
    Actualizar una tarea existente
    ---
    tags:
      - Tasks
    parameters:
      - name: task_id
        in: path
        required: true
        type: string
        description: ID de la tarea a actualizar
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            status:
              type: string
              example: "completed"
    responses:
      200:
        description: Tarea actualizada
      404:
        description: Tarea no encontrada
    """
    data = request.get_json()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = data.get("status", task["status"])
            return jsonify(task), 200
    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    """
    Eliminar una tarea existente
    ---
    tags:
      - Tasks
    parameters:
      - name: task_id
        in: path
        required: true
        type: string
        description: ID de la tarea a eliminar
    responses:
      200:
        description: Tarea eliminada exitosamente
      404:
        description: Tarea no encontrada
    """
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return jsonify({"message": "Task deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
