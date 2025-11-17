from flask import request
from app.db import db
from .route_utilities import validate_model, create_model as util_create_model

def create_model_endpoint(model_cls, required_keys=("title",)):
    body = request.get_json() or {}
    return util_create_model(model_cls, body)

def list_models_endpoint(model_cls):
    return [m.to_dict() for m in model_cls.query.all()]

def get_one_endpoint(model_cls, model_id):
    instance = validate_model(model_cls, model_id)
    return instance.to_dict(), 200

def update_fields_endpoint(instance, fields):
    body = request.get_json() or {}
    for f in fields:
        if f in body:
            setattr(instance, f, body[f])
    db.session.commit()
    return instance.to_dict(), 200

def delete_model_endpoint(instance, success_msg_template):
    db.session.delete(instance)
    db.session.commit()
    return {"details": success_msg_template.format(id=instance.id, title=getattr(instance, "title", ""))}, 200
