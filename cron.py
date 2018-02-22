# Fire once a day.
import os 
import crython

#@crython.job(expr='@daily')
@crython.job(second='*/30')
def cron():
	os.system('python fetch-stats.py')
	print 'cron started'
