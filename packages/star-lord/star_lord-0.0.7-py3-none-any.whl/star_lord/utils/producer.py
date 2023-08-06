# Django
from django.db.models.signals import post_save
from django.forms.models import model_to_dict
from django.conf import settings

# Project
from ..amqp.job import JobClient, job_tasks


def signal_post_save(sender, instance, created, **kwargs):
    instance.send([instance])


def send(routing_key):
    @staticmethod
    def wrapper(instances):
        JobClient().call(routing_key, [model_to_dict(i) for i in instances])

    return wrapper


def sync_model(_, model):
    model.send(model.objects.all())


def producer(model):
    app_name = '%s.%s' % (settings.APP_NAME, model.get_name())
    routing_key = "%s.changed" % app_name

    model.routing_key = routing_key
    model.send = send(model.routing_key)

    job_tasks(app_name, model=model)(sync_model)

    if not hasattr(model, 'signal_post_save'):
        model.signal_post_save = signal_post_save

    post_save.connect(model.signal_post_save, sender=model)
    return model
