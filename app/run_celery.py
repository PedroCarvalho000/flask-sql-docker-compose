# -*- coding: utf-8 -*-

import os

from celery import Celery

from app import create_app


def make_celery(app=None):
    app = app or create_app('celeryapp', os.path.dirname(__file__))
    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    task_base = celery.Task #Alterei as ocorrências desta variavel para snake case pois é apontado como boa prática. Mas creio que não era necessário corrigir pq essa variavel representa um método.

    class ContextTask(task_base):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return task_base.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery
