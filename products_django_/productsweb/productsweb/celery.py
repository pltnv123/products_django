import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'productsweb.settings')

app = Celery('productsweb')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'print_every_5_seconds': {
        'task': 'simpleapp.tasks.printer',
        'schedule': 20,          # переодичность выполнения
        'args': (10,),     # конец счетчика
    },
}