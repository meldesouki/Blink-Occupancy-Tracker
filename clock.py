from apscheduler.schedulers.blocking import BlockingScheduler
from occupancy_tracker import cronjob

scheduler = BlockingScheduler()

# scheduler.add_job(cronjob, 'cron', id = 'main_job', hour = '7-19', minute = 3, timezone= 'America/New_York') #0 , jitter = 300)

@scheduler.scheduled_job('cron', hour = '7-19', minute = 3, timezone= 'America/New_York')
def chronological_job():
    cronjob()

@scheduler.scheduled_job('interval', minutes=2)
def timed_job():
    print('This job is run every two minutes.')

scheduler.start()
