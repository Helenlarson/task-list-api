from flask import Blueprint, request, make_response
from .route_utilities import validate_model
from sqlalchemy import asc, desc
from app.models.task import Task
from ..db import db

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json() or {}

    if "title" not in request_body or "description" not in request_body:
        return {"details": "Invalid data"}, 400

    new_task = Task(
        title=request_body["title"],
        description=request_body["description"],
        completed_at=request_body.get("completed_at")
    )

    db.session.add(new_task)
    db.session.commit()

    return new_task.to_dict(), 201


@tasks_bp.get("")
def get_tasks():
    sort = request.args.get("sort")
    query = db.select(Task)

    if sort == "asc":
        query = query.order_by(asc(Task.title))
    elif sort == "desc":
        query = query.order_by(desc(Task.title))

    # Use the built query (not db.select(Task) again)
    tasks = db.session.scalars(query).all()
    return [task.to_dict() for task in tasks], 200


@tasks_bp.get("/<task_id>")
def get_task(task_id):
    task = validate_model(Task, task_id)
    return task.to_dict(), 200


@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json() or {}

    if "title" not in request_body or "description" not in request_body:
        return {"details": "Invalid data"}, 400

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()
    return make_response("", 204)


@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    return make_response("", 204)
