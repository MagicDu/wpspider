#!/usr/bin/env python3
#-*- coding:utf-8-*-
'''
python 程序定时执行脚本
需要 安装 python-crontab
'''
from crontab import CronTab

'''
cronTab定时执行任务
str_command : 执行的命令（eg: 'python3 /mysoft/py/News_Robot.py')注意执行的目录一定要正确
str_time    : 命令执行的时间（具体请参考 crontab的说明）
'''
def setCronTab(str_command,str_time):
	my_cron=CronTab(user=True)
	job=my_cron.new(str_command)
	job.setall(str_time)
	my_cron.write()

#example   
setCronTab('python3 /mysoft/py/wpspider.py','0 6 * * *')