from flask import Blueprint, request, Response
from ..models.goal import Goal
from ..models.task import Task
from ..db import db
from .route_utilities import validate_model, create_model, get_models_with_filters

bp = Blueprint('goals_bp', __name__, url_prefix='/goals')

# GET /goals  -> 200 []
@goals_bp.get("")
def get_goals():
    goals = db.session.execute(db.select(Goal)).scalars().all()
    return [g.to_dict() for g in goals], 200

# GET /goals/<id>  -> 200 {id,title}  | 404 {"message": "Goal 1 not found"}
@goals_bp.get("/<goal_id>")
def get_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return goal.to_dict(), 200

# POST /goals  -> 201 {id,title} | 400 {"details":"Invalid data"}
@goals_bp.post("")
def create_goal():
    data = request.get_json() or {}
    if "title" not in data:
        return {"details": "Invalid data"}, 400

    new_goal = Goal.from_dict(data)
    db.session.add(new_goal)
    db.session.commit()
    return new_goal.to_dict(), 201

# PUT /goals/<id> -> 200 {id,title} | 400 invalid | 404 not found

@goals_bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    data = request.get_json() or {}
    if "title" not in data:
        return {"details": "Invalid data"}, 400

    goal.title = data["title"]
    db.session.commit()
    return make_response("", 204)   # <<-- Wave 05 espera 204


# DELETE /goals/<id> -> 204 "" | 404 not found
@goals_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()
    return make_response("", 204)
