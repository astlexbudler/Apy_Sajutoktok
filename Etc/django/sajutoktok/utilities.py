import random
import string
import time
import base64
import hmac
import hashlib
import json
import requests
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pyproj import Proj, transform
import haversine
import sys
import os
import google.auth.transport.requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.oauth2 import service_account
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from openai import OpenAI
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from . import models as mo
from . import utilities as ut
from . import daos as do

from colorama import Fore, Back, Style, init
init(autoreset=True)

##################################################
# [utilites.py]
# random
# def get_rand_id(length): # make random id(str + num)
# def get_rand_num(length): # make random number
# def get_rand_str(length): # make random string
# datetime
# def get_now_dt(): # "0000-00-00 00:00"
# def get_datetime_from_dt(dt): # dt String to datetime format
# def get_dt_from_datetime(dt): # datetime to dt String
# messaging
# def send_webpush(title, message, link) # send web push message. no limit.
# def send_message(tel, content): # SMS: length under 70, LMS: no length limit. send phone message(only korean). 10-50KRW/each
# def send_smtp(sender_name, sender_email, to_email, title, html): # SMTP email send. cafe24: smtp.cafe24.com / 587. limit 400/day.(FAST)
# def send_email(sender_email, to_email, title, html) # send email using selenium. no-limit.(SLOW)
# def send_apppush(project_id, title, content, link): # send app push message. no limit.
# def send_notification(title, content, link) # send service's notification. no limit. registered users only.
# encryption
# def encrypt_aes(data): # make data to aes encryption(encrypt)
# def decrypt_aes(data): # get original data from aes encryption(decrypt)
# def encrypt_sha256(data): # make data to sha256 encryption(encrypt). can't decrypt.
# purchase
# def toss_confirm_order(payment_id) # todo
# other
# def get_ip(request): # get user's ip address from request
# def get_ip_lang(ip): # get ip country's language from ipinfo.io
# def print_dict_structure(dict): # print dictionary structure
# def print_debug_info(request, title, context): # print debug info
# def print_info_n_return(request, title, context, path): # print debug info and return context
# def make_dict_to_json(dict): # make dictionary to json String
# def make_json_to_dict(json_string): # read json String to dictionary



##################################################
# random
def get_rand_id(length): # make random id(str + num)
    # first letter is always alphabet
    return ''.join(random.choices(string.ascii_letters, k=1)) + ''.join(random.choices(string.ascii_letters + string.digits, k=length-1))

def get_rand_num(length): # make random number
    # first letter must not be 0.
    return ''.join(random.choices(string.digits[1:], k=1)) + ''.join(random.choices(string.digits, k=length-1))

def get_rand_str(length): # make random string
    return ''.join(random.choices(string.ascii_letters, k=length)).lower()



##################################################
# datetime
def get_now_dt(): # "0000-00-00 00:00"
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def get_full_dt(): # "0000-00-00 00:00:00"
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')

def get_datetime_from_dt(dt): # dt String to datetime format
    return datetime.strptime(dt, "%Y-%m-%d %H:%M")

def get_dt_from_datetime(dt): # datetime to dt String
    return dt.strftime("%Y-%m-%d %H:%M")



##################################################
# messaging
def send_smtp(sender_name, to_email, title, html): # SMTP email send. cafe24: smtp.cafe24.com / 587. limit 400/day.(FAST)    try:
    try:
        # 수정필요
        sender_email = mo.SERVER_SETTING.objects.get(key="SMTP_이메일_아이디").value
        msg = MIMEMultipart()
        msg['From'] = f'{sender_name} <{sender_email}>'
        msg['To'] = to_email
        msg['Subject'] = title
        msg.attach(MIMEText(html, "html"))

        smtp_session = smtplib.SMTP(
            mo.SERVER_SETTING.objects.get(key="SMTP_서버_주소").value,
            mo.SERVER_SETTING.objects.get(key="SMTP_서버_포트").value
        )
        smtp_session.login(
            sender_email,
            mo.SERVER_SETTING.objects.get(key="SMTP_이메일_비밀번호").value
        )
        smtp_session.send_message(msg)
        smtp_session.quit()
    except Exception as e:
        print(f"error: {str(e)}")
    return

def send_apppush(device_tokens, title, message, link): # send app push message. no limit.
    return

def send_webpush(ids, title, message, link): # send web push message. no limit.
    return


##################################################
# other
def get_ip(request): # get user's ip address from request
    return request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')

def print_dict_structure(d): # print dictionary structure
    structure = ""
    try:
        if type(d) == list:
            d = d[0]
        for key, value in d.items():
            if type(value) == dict:
                structure += f"{key}({print_dict_structure(value)}), "
            structure += f"{key}, "
        structure = structure[:-2]
    except:
        pass
    return structure

def print_debug_info(request, title, contexts): # print debug info
    if settings.DEBUG:
        print(f"\n\n\n{Fore.GREEN}[{get_now_dt()}]{title}{Fore.RESET}")
        print(f"{Fore.BLUE}SESSION:{Fore.RESET} {print_dict_structure(request.session)}")
        print(f"{Fore.BLUE}GET:{Fore.RESET} {print_dict_structure(request.GET)}")
        print(f"{Fore.BLUE}POST:{Fore.RESET} {print_dict_structure(request.POST)}")
        print(f"{Fore.LIGHTMAGENTA_EX}contexts:{Fore.RESET} ")
        for key, value in contexts.items():
            print (f"{Fore.LIGHTMAGENTA_EX}{key}:{Fore.RESET} {print_dict_structure(value)}")
    return

def print_info_n_return(request, title, contexts, path): # print debug info and return context
    if settings.DEBUG:
        print(f"\n\n\n{Fore.GREEN}[{get_now_dt()}]{title}{Fore.RESET}")
        print(f"{Fore.BLUE}SESSION:{Fore.RESET} {print_dict_structure(request.session)}")
        print(f"{Fore.BLUE}GET:{Fore.RESET} {print_dict_structure(request.GET)}")
        print(f"{Fore.BLUE}POST:{Fore.RESET} {print_dict_structure(request.POST)}")
        print(f"{Fore.LIGHTMAGENTA_EX}contexts:{Fore.RESET} ")
        for key, value in contexts.items():
            print (f"{Fore.LIGHTMAGENTA_EX}{key}:{Fore.RESET} {print_dict_structure(value)}")
    if request.method == 'POST':
        return JsonResponse(contexts)
    else:
        return render(request, path, contexts)

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return {"__type__": "datetime", "value": obj.strftime('%Y-%m-%d %H:%M:%S')}
        elif isinstance(obj, bytes):
            return {"__type__": "bytes", "value": obj.decode('utf-8', errors='ignore')}
        elif isinstance(obj, int):
            return {"__type__": "int", "value": obj}
        elif isinstance(obj, float):
            return {"__type__": "float", "value": obj}
        elif isinstance(obj, bool):
            return {"__type__": "bool", "value": obj}
        elif obj is None:
            return {"__type__": "none", "value": obj}
        elif isinstance(obj, str) and '"' in obj:
            return {"__type__": "str", "value": obj.replace('"', "'")}
        else:
            return {"__type__": "str", "value": str(obj)}

def json_encorder(dict): # make dictionary to json String
    try:
        return json.dumps(dict, cls=CustomEncoder, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"__type__": "error", "value": str(e)})

def json_decorder(json_string): # read json String to dictionary
    def custom_decoder(obj):
        if "__type__" in obj:
            type_info = obj["__type__"]
            if type_info == "datetime":
                return datetime.strptime(obj["value"], '%Y-%m-%d %H:%M:%S')
            elif type_info == "bytes":
                return obj["value"].encode('utf-8')
            elif type_info == "int":
                return int(obj["value"])
            elif type_info == "float":
                return float(obj["value"])
            elif type_info == "bool":
                return bool(obj["value"])
            elif type_info == "none":
                return None
            else:
                return obj["value"]
        return obj
    try:
        parsed_dict = json.loads(json_string, object_hook=custom_decoder)
        return parsed_dict
    except Exception as e:
        return {"error": str(e)}

