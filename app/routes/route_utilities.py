# app/route_utilities.py
from flask import abort, make_response

def validate_model(model_class, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        abort(make_response({"details": f"{model_class.__name__} {model_id} invalid"}, 400))

    instance = model_class.query.get(model_id)
    if not instance:
        abort(make_response({"details": f"{model_class.__name__} {model_id} not found"}, 404))
    return instance
