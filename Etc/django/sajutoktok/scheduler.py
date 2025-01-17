from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.triggers.interval import IntervalTrigger
from . import models
from datetime import datetime, timedelta
from django.utils import timezone
import requests
from django.db.models import Q
from . import utilities
from . import daos as do



def startScheduler():
    scheduler = BackgroundScheduler()
    #scheduler.add_job(clean_security_tables, 'interval', minutes=30)
    #scheduler.add_job(calc_search_order, 'interval', hours=1)
    #scheduler.add_job(delete_old_messages, 'interval', days=7)
    #scheduler.add_job(refresh_counselor_status, 'interval', minutes=5)
    scheduler.start()



##################################################
# scheduler.py
# def clean_security_tables(): # clean security tables
# def delete_old_messages(): # clean old messages



def clean_security_tables(): # clean security tables
    models.ACCESS_IP.objects.all().delete()
    now_datetime = utilities.get_datetime_from_dt(utilities.get_now_dt())
    certs = models.CERT_CODE.objects.all().order_by('dt')
    thirty_minutes_ago = now_datetime - timedelta(minutes=30)
    for c in certs: # DELETE CERT_CODE
        c_datetime = utilities.get_datetime_from_dt(c.dt)
        if c_datetime < thirty_minutes_ago:
            c.delete()
        else:
            break

def calc_search_order(): # calculate search order
    counselors = do.get_all_counselors()
    for counselor in counselors:
        search_order = 0
        if counselor['status'] == 'busy':
            search_order += 3000
        elif counselor['status'] == 'online':
            search_order += 1500
        search_order += int(counselor['likes'])
        search_order += int(counselor['review_avg']) * 10
        search_order += int(counselor['reviews_count'])
        search_order += int(counselor['weight'])
        counselor = models.ACCOUNT.objects.get(
            id = counselor['id']
        )
        counselor.search_order = search_order
        counselor.save()

def delete_old_messages(): # clean old messages
    now_datetime = utilities.get_datetime_from_dt(utilities.get_now_dt())
    seven_days_ago = now_datetime - timedelta(days=7)
    notifications = models.NOTIFICATION.objects.all().order_by('dt')
    for n in notifications: # DELETE NOTIFICATION
        n_datetime = utilities.get_datetime_from_dt(n.dt)
        if n_datetime < seven_days_ago:
            n.delete()
        else:
            break
    logs = models.LOG.objects.all().order_by('dt')
    for l in logs: # DELETE LOG
        l_datetime = utilities.get_datetime_from_dt(l.dt)
        if l_datetime < seven_days_ago:
            l.delete()
        else:
            break
    thirty_days_ago = now_datetime - timedelta(days=30)
    chats = models.CHAT.objects.all().order_by('dt')
    for c in chats: # DELETE CHAT
        c_datetime = utilities.get_datetime_from_dt(c.dt)
        if c_datetime < thirty_days_ago:
            c.delete()
        else:
            break

def refresh_counselor_status(): # refresh counselor status
    counselors = models.ACCOUNT.objects.exclude(
        status = 'hidden'
    ).filter(
        account_type = 'counselor'
    )
    cp_codes = []

    for counselor in counselors:
        cp_code = counselor.id
        if cp_code not in cp_codes:
            cp_codes.append(cp_code)
            # request 060
            response = requests.get(
                f"http://060300.co.kr/center2/cp_stat2.php?cp_code={cp_code}"
            )
            # 'code': 'status'(0: now_offline, 1: now_online/0: on_working, 1: n/0: not_worktine, 1: worktime)
            # {"001":"111","002":"101","003":"100","004":"000"}
            if response.status_code == 200:
                data = response.json()
                for key, value in data.items():
                    key_account = models.ACCOUNT.objects.filter(
                        account_type = 'counselor',
                        counselor_code = key
                    ).first()
                    if key_account is not None:
                        if value[0] == '1' and key_account.status == 'offline':
                            key_account.status = 'online'
                            key_account.save()
                            models.LOG(
                                log = f"{key_account.nickname}님이 온라인 상태로 변경되었습니다.",
                            ).save()
                        elif value[0] == '0' and key_account.status == 'online':
                            key_account.status = 'offline'
                            key_account.save()
                            models.LOG(
                                log = f"{key_account.nickname}님이 오프라인 상태로 변경되었습니다.",
                            ).save()
            else:
                pass