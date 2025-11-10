from flask import abort, make_response
from app.db import db

def validate_model(model_class, model_id):
    try:
        model_id = int(model_id)
    except (TypeError, ValueError):
        abort(make_response({"details": f"{model_class.__name__} {model_id} invalid"}, 400))

    instance = model_class.query.get(model_id)
    if not instance:
        abort(make_response({"details": f"{model_class.__name__} {model_id} not found"}, 404))
    return instance


def create_model(model_class, request_body):
    if not isinstance(request_body, dict) or not request_body.get("title"):
        abort(make_response({"details": "Invalid data"}, 400))

    instance = model_class.from_dict(request_body)
    db.session.add(instance)
    db.session.commit()
    return instance.to_dict(), 201
