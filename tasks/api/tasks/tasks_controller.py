from flask import request
from .tasks_model import Tasks
from firebase_admin import auth
from functools import wraps
from .validation import valid_task
from mongoengine.errors import DoesNotExist
from tasks import firebase


def valid_token(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if not request.headers.get('authorization'):
            return {"msg":"error","inf": "No token provided", "status": 400}
        try:
            user = auth.verify_id_token(request.headers['authorization'])
            request.user = user
        except:
            return {"msg":"error","inf":"Invalid token provided", "status": 400}
        return f(*args, **kwargs)
    return wrap


@valid_token
def post_tasks(body):
    task = body['task']
    valid = valid_task(task)
    if "error" in valid.keys():
        resp = {
            "msg": "error",
            "inf": valid['error'],
            "status": 400
        }
        return resp

    token = request.headers['authorization']
    decoded_token = auth.verify_id_token(token)
    email = decoded_token['firebase']['identities']['email'][0]
    
    try:
        Tasks.objects(email=email)
        Tasks.objects(email=email).update_one(push__tasks=task)
        x  = Tasks.objects.get(email=email)
        resp = {
            "msg":"success",
            "data":[{
                "email": x["email"],
                "tasks": x["tasks"]
            }], 
            "status": 200
        }
        return resp
    except DoesNotExist:
        Tasks(email=email).save()
        Tasks.objects(email=email).update_one(push__tasks=task)

        x  = Tasks.objects.get(email=email)

        resp = {
            "msg":"success",
            "data":[{
                "email": x["email"],
                "tasks": x["tasks"]
            }], 
            "status": 200
        }
        return resp


@valid_token
def get_tasks():
    token = request.headers['authorization']
    decoded_token = auth.verify_id_token(token)
    email = decoded_token['firebase']['identities']['email'][0]
    
    try:
        tasks = Tasks.objects.get(email=email)
        resp = {
            "msg":"success",
            "data":[{
                "tasks": tasks['tasks']
            }], 
            "status": 200
        }
        return resp
    except DoesNotExist:
        resp = {
            "msg":"error",
            "inf":"Tasks not found", 
            "status": 400
        }
        return resp


@valid_token
def delete_tasks():
    token = request.headers['authorization']
    decoded_token = auth.verify_id_token(token)
    email = decoded_token['firebase']['identities']['email'][0]
    try:
        task = Tasks.objects.get(email=email)
        Tasks.objects(email=email).delete()
        resp = {
            "msg":"success",
            "inf":"Tasks deleted", 
            "status": 200
        }
        return resp

    except DoesNotExist:
        resp = {
            "msg":"error",
            "inf": "Tasks not found", 
            "status": 400
        }
        return resp