from apscheduler.schedulers.blocking import BlockingScheduler
from occupancy_tracker import cronjob

scheduler = BlockingScheduler()

scheduler.add_job(cronjob(), 'cron', day_of_week = '*', hour = '7-19')

scheduler.start()