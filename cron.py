from crontab import CronTab

cron = CronTab()  
job = cron.new(command='python fetch-stats.py')  
job.hour.every(24) # Fire once a day.