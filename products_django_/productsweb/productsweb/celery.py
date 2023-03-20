import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'productsweb.settings')

app = Celery('productsweb')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
