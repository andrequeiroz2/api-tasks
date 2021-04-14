import os
from flask import Flask
from tasks import database
from flask_restful import Api
from tasks.api.tasks.tasks_route import init_tasks_api

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'todo-api/api-taks:1.0'

    app.config['MONGODB_SETTINGS'] = {
         'db': 'tasks',
         'host': 'mongodb://admin:passwordD21@mongodbtasks:27017/tasks?authSource=admin',
         
     }

    database.init_app(app)

    api = Api(app)
    init_tasks_api(api)

    return app