from .tasks_api import TagsApi

def init_tasks_api(api):
    api.add_resource(TagsApi, "/api/users/tasks")