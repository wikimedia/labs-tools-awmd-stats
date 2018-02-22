# Fire once a day.
import os 
import crython

@crython.job(expr='@daily')
def foo():
	os.system('python fetch-stats.py')
