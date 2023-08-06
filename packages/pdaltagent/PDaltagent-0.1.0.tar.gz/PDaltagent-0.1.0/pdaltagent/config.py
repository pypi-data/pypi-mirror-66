from celery import Celery
import redis
import sys
import time

print(f"{time.time()} ping redis")
try:
    r = redis.Redis('localhost')
    r.ping()
except:
    print(f"Redis is not found on 'localhost' - are you sure it's running?")
    sys.exit(1)
print(f"{time.time()} create app")
app = Celery('tasks', 
             backend='redis://localhost:6379/0', 
             broker='redis://localhost:6379/0')
