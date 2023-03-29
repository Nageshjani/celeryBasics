```bash
project/
├── project/
│   ├── __init__.py 
│   ├── settings.py 
│   ├── celery.py 
│   ├── urls.py
|
├── app/
│   └── views.py
│   └── tasks.py
└── manage.py

```




```bash
pip install redis
```
```bash
pip install celery 
```

```bash
django-admin startproject project
```

```bash
cd project
```

```bash
python manage.py startapp app
```


## settings.py
```python
# CELERY_BROKER_URL = 'redis://127.0.0.1:6379' 
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0' 
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['application/json'] 
CELERY_RESULT_SERIALIZER = 'json' 
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'


INSTALLED_APPS = [
   
    'app'
]

```
## REDIS CONFIG

![Screenshot (578)](https://user-images.githubusercontent.com/34247973/228630214-928a8264-d6e1-40fb-9ca9-8113a617caaa.png)

```bash
'Open Your Redis File'
'Double Click on redis-server'
'Double Click on redis-cli'
```

![Screenshot (579)](https://user-images.githubusercontent.com/34247973/228630270-8c455343-3578-4873-b831-f8441d50b8de.png)
![Screenshot (580)](https://user-images.githubusercontent.com/34247973/228630308-07beefa0-99fd-4642-9818-f1ca7517c0fd.png)

```bash
'Type ping in redis-cli'
'You should get PONG in reply'
```

## project/celery.py
```python
import os  
  
from celery import Celery  
from celery.schedules import crontab  

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')  
#os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
app = Celery('project')  
app.config_from_object('django.conf:settings', namespace='CELERY')  
app.autodiscover_tasks()  
  
@app.task(bind=True)  
def debug_task(self):  
    print(f'Request: {self.request!r}')      
```
```bash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')  
'add your project name'
```

```bash
app = Celery('project')  
'Your project_name'
```

## project/init.py 
```python
from .celery import app as celery_app
__all__ = ['celery_app']

```

## app/tasks.py 
```python
from celery import shared_task  
import time
  
@shared_task(bind=True)  
def test_func(self):  
    time.sleep(5)
    for i in range(10):  
        print(i)  
        time.sleep(1)
    return "Completed"  

```   
    
## app/views.py 
```python
from django.shortcuts import render
from django.http import HttpResponse  
from project.tasks import test_func  
  
  
def test(request):  
    test_func.delay()  
    return HttpResponse("Done")
    
```

## project/urls.py  
```python
from app.views import test

urlpatterns = [
    path('',test)
]
```


![Screenshot (581)](https://user-images.githubusercontent.com/34247973/228630419-216ad690-7f72-4ac9-9e44-0ffb3ae35655.png)

```bash
celery -A my_project_name worker --pool=solo -l info
```
```bash
'Add Your Project Name in place of my_project_name'
```

```bash
python manage.py runserver
```

```bash
'go to url http://127.0.0.1:8000/
```

![Screenshot (582)](https://user-images.githubusercontent.com/34247973/228630479-cd62dbe2-5013-4ecf-a274-18acd54878bb.png)
![Screenshot (583)](https://user-images.githubusercontent.com/34247973/228630534-b4add345-6860-44b0-86ff-fb23285ee559.png)

celery -A project worker --pool=solo -l info
