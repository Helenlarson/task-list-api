# app/routes/route_utilities.py
from flask import abort, make_response
from ..db import db

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))

    model = db.session.get(cls, model_id)
    if model is None:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))

    return model


def create_model(cls, request_body):
    """
    Generic helper used by tests in Wave 7.
    Builds a model via cls.from_dict and returns 400 with {"details": "Invalid data"}
    if required fields are missing (KeyError).
    """
    try:
        model = cls.from_dict(request_body)
    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400))
    return model
