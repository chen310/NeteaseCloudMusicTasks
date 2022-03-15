import os
import random
from apscheduler.schedulers.background import BlockingScheduler
from index import start

if __name__ == "__main__":
    try:
        start()
        scheduler_hour = os.environ.get(
            "SCHEDULER_HOUR", random.randint(0, 23))
        scheduler_minute = os.environ.get(
            "SCHEDULER_MINUTE", random.randint(0, 59))
        print("Scheduler hour: %s, minute: %s" %
              (scheduler_hour, scheduler_minute))
        scheduler = BlockingScheduler(timezone='Asia/Shanghai')
        scheduler.add_job(start, 'cron', hour=scheduler_hour,
                          minute=scheduler_minute)
        scheduler.start()
    except Exception as e:
        print(e)
        exit(1)
