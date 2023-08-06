# Project
from ..amqp.job import job_tasks


def sync(model, data):
    model.objects.bulk_data()


def consumer(routing_key: str):
    def wrapper(func):
        task_name = routing_key
        job_tasks(task_name)(func)
        return func

    return wrapper
