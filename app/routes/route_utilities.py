from flask import abort, make_response
from ..db import db

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        abort(make_response({"details": f"{cls.__name__} {model_id} not found"}, 404))

    model = db.session.get(cls, model_id)

    if not model:
        abort(make_response({"details": f"{cls.__name__} {model_id} not found"}, 404))

    return model