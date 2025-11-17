import os
from celery import Celery

# Definindo as configurações do projeto django, passnado para o celery.py qual é o arquivo que possui as configs (banco, apps e etc)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')

# Criando instancia de um objeto celery
app = Celery('setup')

# Busca as configurações do arquivo settings que possuem a nomeclatura "CELERY"
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()