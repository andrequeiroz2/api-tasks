import json
from flask_restful import Resource
from flask import Response, request
from .tasks_controller import (
    
    post_tasks, 
    get_tasks,
    delete_tasks
    
)


class TagsApi(Resource):
    def post(self):
        body = request.get_json()
        rs = post_tasks(body)
        rj = json.dumps(rs)
        return Response(rj, mimetype="application/json", status=rs['status'])
    
    def get(self):
        rs = get_tasks()
        rj = json.dumps(rs)
        return Response(rj, mimetype="application/json", status=rs['status'])
    
    def delete(self):
        rs = delete_tasks()
        rj = json.dumps(rs)
        return Response(rj, mimetype="application/json", status=rs['status'])