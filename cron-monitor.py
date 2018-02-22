from crontab import CronTab

cron = CronTab()  
for job in cron:  
    print (job)
