from celery import shared_task  
import time
  
@shared_task(bind=True)  
def test_func(self):  
    time.sleep(5)
    for i in range(10):  
        print(i)  
        time.sleep(1)
    return "Completed"  