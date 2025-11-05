from flask import Blueprint, request, make_response, abort
from ..models.task import Task
from ..db import db

# use o mesmo nome (tasks_bp) em tudo
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json() or {}

    if "title" not in request_body or "description" not in request_body:
        return {"details": "Invalid data"}, 400

    new_task = Task(
        title=request_body["title"],
        description=request_body["description"],
        completed_at=None,
    )

    db.session.add(new_tasks)
    db.session.commit()

    response = {
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "is_completed": False,
    }

    return response, 201

@tasks_bp.get("")
def get_tasks():
    tasks = db.session.scalars(db.select(Task)).all()

    response = []
    for task in tasks:
        response.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_completed": task.completed_at is not None,
        })

    return response, 200

@tasks_bp.get("/<task_id>")
def get_task(task_id):
    task = validate_model(Task, task_id)
    response = {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_completed": task.completed_at is not None,
    }

    return response, 200

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return {"details": "Invalid data"}, 400

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response("", 204)