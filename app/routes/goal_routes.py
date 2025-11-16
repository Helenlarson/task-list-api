# app/routes/goal_routes.py
from flask import Blueprint, request
from app.models.goal import Goal
from app.models.task import Task
from app.db import db
from .route_utilities import validate_model

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.post("")
def create_goal():
    body = request.get_json() or {}
    if "title" not in body or not body["title"]:
        return {"details": "Invalid data"}, 400
    goal = Goal(title=body["title"])
    db.session.add(goal)
    db.session.commit()
    return goal.to_dict(), 201

@goals_bp.get("")
def get_all_goals():
    goals = Goal.query.all()
    return [g.to_dict() for g in goals]

@goals_bp.post("/<goal_id>/tasks")
def assign_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    body = request.get_json() or {}
    task_ids = body.get("task_ids")
    if not isinstance(task_ids, list):
        return {"details": "Invalid data"}, 400
    goal.tasks = []
    tasks = []
    for tid in task_ids:
        task = validate_model(Task, tid)
        task.goal = goal
        tasks.append(task)
    db.session.commit()
    return {"id": goal.id, "task_ids": [t.id for t in tasks]}, 200

@goals_bp.get("/<goal_id>/tasks")
def get_tasks_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    response = goal.to_dict()
    response["tasks"] = [t.to_dict() for t in goal.tasks]
    return response

@goals_bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return goal.to_dict()

@goals_bp.put("/<goal_id>")
def update_goal_title(goal_id):
    goal = validate_model(Goal, goal_id)
    body = request.get_json() or {}
    if "title" not in body or not body["title"]:
        return {"details": "Invalid data"}, 400
    goal.title = body["title"]
    db.session.commit()
    return goal.to_dict()