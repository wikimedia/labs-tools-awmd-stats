from crontab import CronTab

cron = CronTab()  
job = cron.new(command='python fetch-stats.py')  
job.minute.every(1)

cron.write() 