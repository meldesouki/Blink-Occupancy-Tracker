from apscheduler.schedulers.blocking import BlockingScheduler
from occupancy_tracker import cronjob

scheduler = BlockingScheduler()

# scheduler.add_job(cronjob, 'cron', id = 'main_job', hour = '7-19', minute = 3, timezone= 'America/New_York') #0 , jitter = 300)

@scheduler.scheduled_job('cron', id="job_1", hour = '7-19', minute = 3, timezone= 'America/New_York')
def chronological_job():
    cronjob()

scheduler.start()
