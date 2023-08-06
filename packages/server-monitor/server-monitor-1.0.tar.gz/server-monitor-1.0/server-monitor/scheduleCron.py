import os
from crontab import CronTab

import getpass


def get_current_cron_jobs():
    my_cron = CronTab(user=getpass.getuser())
    for job in my_cron:
        print(job)


def is_cron_job_present_or_not(comment):
    my_cron = CronTab(user=getpass.getuser())
    for job in my_cron:
        if job.comment == comment:
            return True
    return False


def creating_new_cron_job(mode,user_id, file_name, name_of_job, minute='*', hour='*', day_of_month='*', month='*', day_of_week='*'):
    # Need to check how to determine if python3 or python to be put
    try:
        my_cron = CronTab(user=getpass.getuser())
        name_of_job += ' #set by Bot'
        job = my_cron.new(command='python3 {} --user_id {} --mode {}'.format(file_name, user_id, mode), comment=name_of_job)
        if minute != '*':
            job.minute.every(minute)
        if hour != '*':
            job.hour.every(hour)
        if day_of_month != '*':
            job.month.every(day_of_month)
        if month != "*":
            job.day.every(month)
        # if day_of_week != "*":
        my_cron.write()

        return True
    except Exception as e:
        print(e)
        return False


def editing_a_cron_job(name_of_job, minute='*', hour='*', day_of_month='*', month='*', day_of_week='*'):
    try:
        my_cron = CronTab(user=getpass.getuser())
        for job in my_cron:
            if job.comment == name_of_job:
                if minute != '*':
                    job.minute.every(minute)
                if hour != '*':
                    job.hour.every(hour)
                if day_of_month != '*':
                    job.month.every(day_of_month)
                if month != "*":
                    job.day.every(month)
                my_cron.write()
                print('Cron job modified successfully')
                return True    
    except Exception as e:
        print(e)
    return False

def deleting_a_cron_job(name_of_comment):
    my_cron = CronTab(user=getpass.getuser())
    check = 0
    for job in my_cron:
        if job.comment == name_of_comment:
            check = 1
            my_cron.remove(job)
            my_cron.write()
    
    if check == 1:
        return True
    else:
        return False

def deleting_all_cron_jobs():
    try:
        my_cron = CronTab(user=getpass.getuser())
        for job in my_cron:
            string = job.comment
            if string[len(string)-12:] == ' #set by Bot':
                my_cron.remove(job)
                my_cron.write()
        return True
    except Exception as e:
        print(e)
    return False
    
# creating_new_cron_job('cron_jobs.py', 'first_job', 1)
# get_current_cron_jobs()

#print(is_cron_job_present_or_not('first_job'))