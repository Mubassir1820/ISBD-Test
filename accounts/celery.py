import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ISBD-Test.settings')

app = Celery('ISBD-Test')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()