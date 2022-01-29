from apscheduler.schedulers.blocking import BlockingScheduler
from occupancy_tracker import get_current_occupancy

sched = BlockingScheduler()


@sched.scheduled_job('cron', hour = '7-19', minute = '0-59/30', timezone = 'America/New_York')
def scheduled_job():
    get_current_occupancy('Woodside')
    get_current_occupancy('Jackson Heights')

sched.start()