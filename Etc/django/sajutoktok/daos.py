import json
from django.shortcuts import render, redirect
from . import models as mo
from django.db.models import Q
from . import utilities
from datetime import datetime, time, timedelta
from itertools import groupby
from operator import attrgetter

from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model, authenticate, login, update_session_auth_hash, logout


##########
# dao
def get_account(email):
  if email == '':
    return None
  User = get_user_model()
  user = User.objects.filter(email=email).first()
  if user is None:
    return None
  user_data = json.loads(user.user_data)
  return {
    'email': user.email,
    'name': user.first_name,
    'nickname': user.last_name,
    'date_joined': datetime.strftime(user.date_joined, '%Y-%m-%d %H:%M:%S'),
    'last_login': datetime.strftime(user.last_login, '%Y-%m-%d %H:%M:%S'),
    'device_token': user_data['device_token'],
    'push_allow': user_data['push_allow'],
    'ad_allow': user_data['ad_allow'],
    'type': user_data['type'],
    'account_status': user_data['account_status'],
    'counselor_categories': str(user_data['counselor_categories']).split(','),
    'counselor_services': str(user_data['counselor_services']).split(','),
    'online_auto_schedule_time': user_data['online_auto_schedule_time'],
    'online_auto_schedule_toggle': user_data['online_auto_schedule_toggle'],
    'offline_auto_schedule_time': user_data['offline_auto_schedule_time'],
    'offline_auto_schedule_toggle': user_data['offline_auto_schedule_toggle'],
    'online_status': user_data['online_status'],
    'point': user_data['point'],
    'accumulated_point': user_data['accumulated_point'],
    'tel': user_data['tel'],
    'address': user_data['address'],
    'weight': user_data['weight'],
    'profile_image_path': user_data['profile_image_path'],
    'introduce': user_data['introduce'],
    'detail': user_data['detail'],
    'like_users': str(user_data['like_users']).split(','),
    'supervisor_note': user_data['supervisor_note'],
  }

def get_notifications(email):
  nos = mo.NOTIFICATION.objects.filter(
    account_id = email,
  ).order_by('-dt')
  return[{
    'id': no.id,
    'title': no.title,
    'content': no.content,
    'link': no.link,
    'dt': no.dt,
  } for no in nos]

def get_settings():
  # 모든 사용자에게 공통으로 적용되는 설정
  service_name = mo.SERVER_SETTING.objects.filter(
    key = '서비스_이름',
  ).first()
  service_logo = mo.SERVER_SETTING.objects.filter(
    key = '서비스_로고',
  ).first()
  company_address = mo.SERVER_SETTING.objects.filter(
    key = '회사_주소',
  ).first()
  company_tel = mo.SERVER_SETTING.objects.filter(
    key = '회사_전화번호',
  ).first()
  company_email = mo.SERVER_SETTING.objects.filter(
    key = '회사_이메일',
  ).first()
  company_name = mo.SERVER_SETTING.objects.filter(
    key = '회사_이름',
  ).first()
  return {
    'service_name': service_name.value,
    'service_logo': service_logo.value,
    'company_address': company_address.value,
    'company_tel': company_tel.value,
    'company_email': company_email.value,
    'company_name': company_name.value,
  }











'''

def get_account(account_id): # get account(user or counselor)
    try:
        ac = mo.ACCOUNT.objects.get(
            id = account_id,
        )
        if ac.account_type == 'user':
            account_data = {
                'id': ac.id,
                'tel': ac.tel,
                'nickname': ac.nickname,
                'account_type': ac.account_type,
                'status': ac.status,
                'device_token': ac.device_token,
                'bookmarks': [],
                'bookmark_ids': str(ac.bookmarks).split(','),
                'point': ac.point,
                'address': ac.address,
            }
            # bookmarks
            bookmarks = str(ac.bookmarks).split(',')
            for bo in bookmarks:
                counselor = get_account(bo)
                if counselor['id'] != '':
                    account_data['bookmarks'].append(counselor)
        if ac.account_type == 'counselor':
            account_data = {
                'id': ac.id,
                'email': ac.email,
                'tel': ac.tel,
                'nickname': ac.nickname,
                'account_type': ac.account_type,
                'status': ac.status,
                'device_token': ac.device_token,
                'photo': ac.photo,
                'services': str(ac.services).split(','),
                'categories': str(ac.categories).split(','),
                'point': ac.point,
                'likes': ac.likes,
                'introduce': ac.introduce,
                'detail': ac.detail,
                'weight': ac.weight,
                'address': ac.address,
                'dt': ac.dt,
                'reviews_count': 0,
                'review_avg': 0,
            }
            # reviews_count
            account_data['reviews_count'] = mo.REVIEW.objects.filter(
                counselor_id = ac.id,
            ).count()
            # review_avg
            reviews = mo.REVIEW.objects.filter(
                counselor_id = ac.id,
            )
            if len(reviews) > 0:
                sum_star = 0
                for re in reviews:
                    sum_star += re.star
                account_data['review_avg'] = round(sum_star / len(reviews), 1)
        if ac.account_type == 'supervisor':
            account_data = {
                'id': ac.id,
                'account_type': ac.account_type,
                'status': ac.status,
                'device_token': ac.device_token,
                'nickname': ac.nickname,
            }
        return account_data
    except Exception as e:
        print("get_account error: ", e)
        return {
            'id': '',
            'account_type': '',
        }

def get_post(post_id): # get post
    try:
        po = mo.POST.objects.get(
            id = post_id,
        )
        post_data = {
            'id': po.id,
            'author': {},
            'target': {},
            'main_image': po.main_image,
            'board': po.board,
            'title': po.title,
            'content': po.content,
            'dt': po.dt,
            'views': po.views,
            'comments': [],
        }
        # author
        post_data['author'] = get_account(po.author_id)
        # target
        post_data['target'] = get_account(po.target_id)
        # comments
        post_data['comments'] = get_comments(post_id)
        return post_data
    except Exception as e:
        print("get_post error: ", e)
        return {
            'id': '',
        }

def get_comment(comment_id): # get comment
    try:
        co = mo.COMMENT.objects.get(
            id = comment_id,
        )
        comment_data = {
            'id': co.id,
            'author': {},
            'content': co.content,
            'dt': co.dt,
        }
        # author
        comment_data['author'] = get_account(co.author_id)
        return comment_data
    except Exception as e:
        print("get_comment error: ", e)
        return {
            'id': '',
        }

def get_review(review_id): # get review
    try:
        re = mo.REVIEW.objects.get(
            id = review_id,
        )
        review_data = {
            'id': re.id,
            'user': {},
            'counselor': {},
            'purchase': {},
            'star': re.star,
            'content': re.content,
            'dt': re.dt,
        }
        # user
        review_data['user'] = get_account(re.user_id)
        if review_data['user']['id'] == '':
            review_data['user'] = {
                'id': '',
                'nickname': re.user_id,
            }
        # counselor
        review_data['counselor'] = get_account(re.counselor_id)
        # purchase
        review_data['payment'] = get_purchase(re.payment_id)
        return review_data
    except Exception as e:
        print("get_review error: ", e)
        return {
            'id': ''
        }

def get_purchase(purchase_id): # get purchase
    try:
        purchase = mo.PURCHASE.objects.get(
            id = purchase_id,
        )
        purchase_data = {
            'id': purchase.id,
            'item': {},
            'user': {},
            'price': purchase.price,
            'duration_seconds': purchase.duration_seconds,
            'dt': purchase.dt,
            'pgcode': purchase.pgcode,
            'cid': purchase.cid,
            'tid': purchase.tid,
            'status': purchase.status,
            'log': purchase.log,
            'token': purchase.token,
        }
        # item
        purchase_data['item'] = get_item(purchase.item_id)
        # user
        purchase_data['user'] = get_account(purchase.user_id)
        return purchase_data
    except Exception as e:
        print("get_purchase error: ", e)
        return {
            'id': ''
        }

def get_cash_item(id): # get cash item
    try:
        ci = mo.SERVER_SETTING.objects.filter(
            id = 'CASH_ITEM_' + id,
        ).first()
        if ci is None:
            if id == '1':
                ci = mo.SERVER_SETTING(
                    id = 'CASH_ITEM_' + id,
                    value = json.dumps({
                        'id': 1,
                        'name': '10,000 + 100 포인트',
                        'description': '사주톡톡에서 사용하는 포인트를 충전합니다. (10,000원)',
                        'price': 10000,
                        'point': 10100,
                    }),
                )
            elif id == '2':
                ci = mo.SERVER_SETTING(
                    id = 'CASH_ITEM_' + id,
                    value = json.dumps({
                        'id': 2,
                        'name': '30,000 + 500 포인트',
                        'description': '사주톡톡에서 사용하는 포인트를 충전합니다. (30,000원)',
                        'price': 30000,
                        'point': 30500,
                    }),
                )
            elif id == '3':
                ci = mo.SERVER_SETTING(
                    id = 'CASH_ITEM_' + id,
                    value = json.dumps({
                        'id': 3,
                        'name': '50,000 + 1,000 포인트',
                        'description': '사주톡톡에서 사용하는 포인트를 충전합니다. (50,000원)',
                        'price': 50000,
                        'point': 51000,
                    }),
                )
            elif id == '4':
                ci = mo.SERVER_SETTING(
                    id = 'CASH_ITEM_' + id,
                    value = json.dumps({
                        'id': 4,
                        'name': '100,000 + 3,000 포인트',
                        'description': '사주톡톡에서 사용하는 포인트를 충전합니다. (100,000원)',
                        'price': 100000,
                        'point': 103000,
                    }),
                )
            ci.save()
        cash_item = {
            'id': id,
            'name': json.loads(ci.value)['name'],
            'description': json.loads(ci.value)['description'],
            'price': json.loads(ci.value)['price'],
            'point': json.loads(ci.value)['point'],
        }
        return cash_item
    except Exception as e:
        print("get_cash_item error: ", e)
        return {
            'id': '',
        }

def get_cash_items(): # get cash items
    try:
        cash_items = []
        for i in range(1, 5):
            cash_items.append(get_cash_item(str(i)))
        return cash_items
    except Exception as e:
        print("get_cash_items error: ", e)
        return []

def get_purchase_terms(): # get purchase terms
    try:
        pt = mo.SERVER_SETTING.objects.filter(
            id = 'PURCHASE_TERMS',
        ).first()
        if pt is None:
            pt = mo.SERVER_SETTING(
                id = 'PURCHASE_TERMS',
                value = '관리자 페이지 > 설정에서 구매 및 환불 처리 약관을 작성해주세요.',
            )
            pt.save()
        purchase_terms = {
            'terms': pt.value,
        }
        return purchase_terms
    except Exception as e:
        print("get_purchase_terms error: ", e)
        return {
            'terms': '',
        }

def get_item(item_id): # get item
    try:
        it = mo.ITEM.objects.get(
            id = item_id,
        )
        item_data = {
            'id': it.id,
            'name': it.name,
            'service': it.item_service,
            'category': str(it.item_category).split(','),
            'provider': {},
            'photos': str(it.photos).split(','),
            'description': it.description,
            'price': it.price,
        }
        # provider
        item_data['provider'] = get_account(it.provider_id)
        return item_data
    except Exception as e:
        print("get_item error: ", e)
        return {
            'id': ''
        }

def get_notification(notification_id): # get notification
    try:
        no = mo.NOTIFICATION.objects.get(
            id = notification_id,
        )
        notification_data = {
            'id': no.id,
            'title': no.title,
            'content': no.content,
            'link': no.link,
            'dt': no.dt,
        }
        return notification_data
    except Exception as e:
        print("get_notification error: ", e)
        return {
            'id': ''
        }

def get_chat(chat_id): # get chat
    try:
        ch = mo.CHAT.objects.get(
            id = chat_id,
        )
        chat_data = {
            'id': ch.id,
            'from': {},
            'to': {},
            'chat_type': ch.chat_type,
            'content': ch.content,
            'read': ch.read,
            'chat_type': ch.chat_type,
            'dt': ch.dt,
            'short_dt': ch.dt[:16],
        }
        # from
        chat_data['from'] = get_account(ch.from_id)
        # to
        chat_data['to'] = get_account(ch.to_id)
        # chat_type
        if ch.chat_type == 'item':
            chat_data['content'] = get_item(ch.content)
        if ch.chat_type == 'purchase':
            chat_data['content'] = get_purchase(ch.content)
        return chat_data
    except Exception as e:
        print("get_chat error: ", e)
        return {
            'id': ''
        }

##########
# list
def get_comments(post_id):
    try:
        comments = []
        cos = mo.COMMENT.objects.filter(
            post_id = post_id,
        ).order_by('dt')
        for co in cos:
            comments.append(get_comment(co.id))
        return comments
    except Exception as e:
        print(e)
        return []

def get_all_users():
    try:
        users = []
        us = mo.ACCOUNT.objects.filter(
            account_type = 'user',
        ).order_by('-dt')
        for u in us:
            users.append(get_account(u.id))
        return users
    except Exception as e:
        print(e)
        return []

def get_users(page):
    try:
        users = []
        us = mo.ACCOUNT.objects.exclude(
            status = 'deleted'
        ).filter(
            account_type = 'user',
        ).order_by('-dt')[(page-1)*10:page*10]
        for u in us:
            users.append(get_account(u.id))
        return users
    except Exception as e:
        print(e)
        return []

def get_all_counselors():
    try:
        counselors = []
        cos = mo.ACCOUNT.objects.filter(
            account_type = 'counselor',
        ).order_by('-search_order', '-likes')
        for co in cos:
            counselors.append(get_account(co.id))
        return counselors
    except Exception as e:
        print(e)
        return []

def get_counselors(category, service, keyword, page):
    try:
        counselors = []

        # search
        cos = mo.ACCOUNT.objects.exclude(
            status = 'hidden'
        )
        # category
        cos = cos.filter(
            Q(categories__contains=category),
            account_type = 'counselor',
        )
        # service
        if service != '' or service != 'all':
            cos = cos.filter(
                Q(services__contains=service),
            )
        # keyword
        if keyword != '':
            cos = cos.filter(
                Q(nickname__contains=keyword),
            )
        # order and page
        cos.order_by('-search_order', '-likes')[(page-1)*10:page*10]

        for co in cos:
            counselors.append(get_account(co.id))
        return counselors
    except Exception as e:
        print(e)
        return []

def get_reviews(page):
    try:
        reviews = []
        res = mo.REVIEW.objects.all().order_by('-dt')[(page-1)*10:page*10]
        for re in res:
            reviews.append(get_review(re.id))
        return reviews
    except Exception as e:
        print(e)
        return []

def get_counselor_reviews(counselor_id, page):
    try:
        reviews = []
        res = mo.REVIEW.objects.filter(
            counselor_id = counselor_id,
        ).order_by('-dt')[(page-1)*10:page*10]
        for re in res:
            reviews.append(get_review(re.id))
        return reviews
    except Exception as e:
        print(e)
        return []

def get_user_reviews(user_id):
    try:
        reviews = []
        res = mo.REVIEW.objects.filter(
            user_id = user_id,
        ).order_by('-dt')
        for re in res:
            reviews.append(get_review(re.id))
        return reviews
    except Exception as e:
        print(e)
        return []

def get_all_notices():
    try:
        notices = []
        nos = mo.POST.objects.filter(
            board = 'notice',
        ).order_by('-dt')
        for no in nos:
            notices.append(get_post(no.id))
        return notices
    except Exception as e:
        print("get_all_notices error: ", e)
        return []

def get_all_events():
    try:
        events = []
        evs = mo.POST.objects.filter(
            board = 'event',
        ).order_by('-dt')
        for ev in evs:
            event = get_post(ev.id)
            events.append(event)
        return events
    except Exception as e:
        print("get_all_events error: ", e)
        return []

def get_user_qnas(user_id):
    try:
        qnas = []
        qas = mo.POST.objects.filter(
            author_id = user_id,
            board = 'qna',
        ).order_by('-dt')
        for qa in qas:
            qnas.append(get_post(qa.id))
        return qnas
    except Exception as e:
        print(e)
        return []

def get_counselor_qnas(counselor_id, page):
    try:
        qnas = []
        qas = mo.POST.objects.filter(
            target_id = counselor_id,
            board = 'qna',
        ).order_by('-dt')
        if page != 'all':
            qas = qas[(page-1)*10:page*10]
        for qa in qas:
            qna = get_post(qa.id)
            qnas.append(qna)
        return qnas
    except Exception as e:
        print("get_counselor_qnas error: ", e)
        return []

def get_all_counselor_qnas(counselor_id):
    try:
        qnas = []
        qas = mo.POST.objects.filter(
            Q(title__contains=f"{counselor_id},"),
            board = 'qna',
        ).order_by('-dt')
        for qa in qas:
            qna = get_post(qa.id)
            qna['title'] = qa.title.split(',')[1]
            qnas.append(qna)
        return qnas
    except Exception as e:
        print(e)
        return []

def get_counselor_blogs(counselor_id, page):
    try:
        blogs = []
        bos = mo.POST.objects.filter(
            author_id = counselor_id,
            board = 'blog',
        ).order_by('-dt')[(page-1)*10:page*10]
        for bo in bos:
            blogs.append(get_post(bo.id))
        return blogs
    except Exception as e:
        print(e)
        return []

def get_all_counselor_blogs(counselor_id):
    try:
        blogs = []
        bos = mo.POST.objects.filter(
            author_id = counselor_id,
            board = 'blog',
        ).order_by('-dt')
        for bo in bos:
            blogs.append(get_post(bo.id))
        return blogs
    except Exception as e:
        print(e)
        return []

def get_notifications(account_id):
    try:
        notifications = []
        nots = mo.NOTIFICATION.objects.filter(
            account_id = account_id,
        ).order_by('-dt')
        for noti in nots:
            notifications.append(get_notification(noti.id))
        return notifications
    except Exception as e:
        print(e)
        return []

def get_chat_rooms(account_id):
    try:
        chat_rooms = []
        cs = mo.CHAT.objects.filter(
            Q(from_id=account_id) | Q(to_id=account_id),
        ).order_by('from_id', 'dt')
        # make 2d array by from_account
        chats_by_from_account = []
        for key, group in groupby(cs, key=attrgetter("from_id")):
            chats_by_from_account.append(list(group))
        # make chats_data
        for chats in chats_by_from_account:
            if chats[0].from_id != account_id:
                chat_rooms.append({
                    "account": get_account(chats[0].from_id),
                    "last_chat": get_chat(chats[-1].id),
                })
                if chat_rooms[-1]["last_chat"]['chat_type'] == 'item':
                    chat_rooms[-1]["last_chat"]['content'] = chat_rooms[-1]["last_chat"]['content']['name']
                elif chat_rooms[-1]["last_chat"]['chat_type'] == 'purchase':
                    chat_rooms[-1]["last_chat"]['content'] = chat_rooms[-1]["last_chat"]['content']['log']
                elif chat_rooms[-1]["last_chat"]['chat_type'] == 'media':
                    chat_rooms[-1]["last_chat"]['content'] = '[이미지 파일]'
                else:
                    last_chat = chat_rooms[-1]["last_chat"]['content']
                    if len(last_chat) > 20:
                        last_chat = last_chat[:20] + '...'
                    chat_rooms[-1]["last_chat"]['content'] = last_chat
        return chat_rooms
    except Exception as e:
        print(e)
        return []

def get_chats(me_id, opponent_id):
    try:
        chats = []
        cs = mo.CHAT.objects.filter(
            Q(from_id=me_id, to_id=opponent_id) | Q(from_id=opponent_id, to_id=me_id),
        ).order_by('dt')
        for c in cs:
            chats.append(get_chat(c.id))
        return chats
    except Exception as e:
        print(e)
        return []

def get_all_purchases():
    try:
        purchases = []
        pus = mo.PURCHASE.objects.all().order_by('-dt')
        for pu in pus:
            purchases.append(get_purchase(pu.id))
        return purchases
    except Exception as e:
        print(e)
        return []

def get_user_purchases(user_id):
    try:
        purchases = []
        pus = mo.PURCHASE.objects.filter(
            user_id = user_id,
        ).order_by('-dt')
        for pu in pus:
            purchases.append(get_purchase(pu.id))
        return purchases
    except Exception as e:
        print(e)
        return []

def get_counselor_purchases(counselor_id, page):
    try:
        purchases = []
        pus = mo.PURCHASE.objects.filter(
            user_id = counselor_id,
        ).order_by('-dt')
        for pu in pus:
            purchases.append(get_purchase(pu.id))
        return purchases[(page-1)*10:page*10]
    except Exception as e:
        print(e)
        return []

def get_items(item_type):
    try:
        items = []
        its = mo.ITEM.objects.filter(
            item_service = item_type,
        )
        for it in its:
            items.append(get_item(it.id))
        return items
    except Exception as e:
        print(e)
        return []

def get_market_items():
    try:
        items = []
        its = mo.ITEM.objects.filter(
            item_service = 'item',
        )
        for it in its:
            items.append(get_item(it.id))
        return items
    except Exception as e:
        print(e)
        return []

def get_counselor_items(counselor_id):
    try:
        items = []
        its = mo.ITEM.objects.filter(
            provider_id = counselor_id,
        )
        for it in its:
            items.append(get_item(it.id))
        return items
    except Exception as e:
        print(e)
        return []



        
        '''