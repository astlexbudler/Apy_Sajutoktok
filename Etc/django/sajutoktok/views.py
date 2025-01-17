import datetime
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from . import models as mo
from . import utilities as ut
from . import daos as do

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

def get_default_contexts(request):
    if request.user.is_authenticated:
        email = request.user.email
    else:
        email = ''
    return {
        'account': do.get_account(email),
        'notifications': do.get_notifications(email),
        'settings': do.get_settings(),
    }

#########
# views.py
# 시작 페이지
# 전화상담, 채팅상담, 대면상담, 카페상담, 점사마켓, 공지사항, 이벤트, 리뷰, 포인트 상점 메뉴 구성
def index(request):
    contexts = get_default_contexts(request)

    return ut.print_info_n_return(request, 'def index(request): # Main', contexts, 'sajutoktok/index.html')

def notices(request): # Notice post list
    account = get_account(request)
    notifications = get_notifications(request)

    # contexts
    notices = do.get_all_notices()
    contexts = {
        'account': account,
        'notifications': notifications,

        'notices': notices,
    }

    return ut.print_info_n_return(request, 'def notices(request): # Notice post list', contexts, 'sajutoktok/notices.html')

def notice(request): # Notice post detail
    account = get_account(request)
    notifications = get_notifications(request)

    # data
    id = request.GET.get('id', '') # notice id

    # contexts
    notice = do.get_post(id)
    if notice['id'] == '':
        return redirect('/notices')
    update_post_views(request, notice) # update post views

    contexts = {
        'account': account,
        'notifications': notifications,

        'notice': notice,
    }

    return ut.print_info_n_return(request, 'def notice(request): # Notice post detail', contexts, 'sajutoktok/notice.html')

def events(request): # Event post list
    account = get_account(request)
    notifications = get_notifications(request)

    # contexts
    events = do.get_all_events()
    contexts = {
        'account': account,
        'notifications': notifications,

        'events': events,
    }

    return ut.print_info_n_return(request, 'def events(request): # Event post list', contexts, 'sajutoktok/events.html')

def event(request): # Event post detail
    account = get_account(request)
    notifications = get_notifications(request)

    # data
    id = request.GET.get('id', '') # event id

    # contexts
    event = do.get_post(id)
    update_post_views(request, event) # update post views
    if event['id'] == '':
        return redirect('/')
    contexts = {
        'account': account,
        'notifications': notifications,

        'event': event,
    }

    return ut.print_info_n_return(request, 'def event(request): # Event post detail', contexts, 'sajutoktok/event.html')

def all_reviews(request): # All Reviews
    account = get_account(request)
    notifications = get_notifications(request)

    # data
    page = request.GET.get('page', 1) # review list page

    # contexts
    reviews = do.get_reviews(page)
    contexts = {
        'account': account,
        'notifications': notifications,

        'reviews': reviews,
    }

    return ut.print_info_n_return(request, 'def all_reviews(request): # All Reviews', contexts, 'sajutoktok/all_reviews.html')

def point_shop(request): # Point Shop
    account = get_account(request)
    notifications = get_notifications(request)

    if account['id'] == '':
        return redirect('login')
    if account['account_type'] == 'counselor':
        return redirect('profile_counselor')

    # contexts
    cash_items = do.get_cash_items()
    contexts = {
        'account': account,
        'notifications': notifications,

        'cash_items': cash_items,
    }

    return ut.print_info_n_return(request, 'def point_shop(request): # point shop', contexts, 'sajutoktok/point_shop.html')

def point_shop_purchase(request): # Point Shop Purchase
    account = get_account(request)
    notifications = get_notifications(request)

    if account['id'] == '':
        return redirect('login')
    if account['account_type'] == 'counselor':
        return redirect('profile_counselor')

    # data
    id = request.GET.get('id', '0')
    cash_item = do.get_cash_item(id)
    if cash_item['id'] == '':
        return redirect('point_shop')
    purchase_terms = do.get_purchase_terms()
    # contexts
    contexts = {
        'account': account,
        'notifications': notifications,

        'cash_item': cash_item,
        'purchase_terms': purchase_terms,
    }

    return ut.print_info_n_return(request, 'def point_shop_purchase(request): # Point Shop Purchase', contexts, 'sajutoktok/point_shop_purchase.html')

def point_shop_purchase_confirm(request): # Point Shop Purchase Confirm
    account = get_account(request)
    notifications = get_notifications(request)

    if account['id'] == '':
        return redirect('login')
    if account['account_type'] == 'counselor':
        return redirect('profile_counselor')

    # contexts
    contexts = {
        'account': account,
        'notifications': notifications,
    }

    return ut.print_info_n_return(request, 'def point_shop_purchase_confirm(request): # Point Shop Purchase Confirm', contexts, 'sajutoktok/point_shop_purchase_confirm.html')

def point_shop_purchase_cancel(request): # Point Shop Purchase Cancel
    account = get_account(request)
    notifications = get_notifications(request)

    if account['id'] == '':
        return redirect('login')
    if account['account_type'] == 'counselor':
        return redirect('profile_counselor')

    # contexts
    contexts = {
        'account': account,
        'notifications': notifications,
    }

    return ut.print_info_n_return(request, 'def point_shop_purchase_cancel(request): # Point Shop Purchase Cancel', contexts, 'sajutoktok/point_shop_purchase_cancel.html')

def purchase_callback(request): # Purchase Callback
    gets = request.GET
    posts = request.POST

    mo.LOG(
        log = f"purchase_callback: {gets} {posts}",
    )

    return HttpResponse()

def purchase_detail(request): # Purchase Detail
    purchase = do.get_purchase(request.GET.get('id', ''))
    return render(request, 'sajutoktok/purchase_detail.html', {'purchase': purchase})

def search(request): # Search
    account = get_account(request)
    notifications = get_notifications(request)

    # data
    category = request.GET.get('category', '') # tel, chat, meet, cafe
    service = request.GET.get('service', '') # taro, saju, jum
    keyword = request.GET.get('keyword', '') # counselor name keyword
    page = request.POST.get('page', 1) # counselor list page
    counselors = do.get_counselors(category, service, keyword, page)

    # contexts
    notices = do.get_all_notices()[:5]
    events = do.get_all_events()
    contexts = {
        'account': account,
        'notifications': notifications,

        'notices': notices,
        'events': events,
        'counselors': counselors,
    }

    return ut.print_info_n_return(request, 'def search(request): # Search', contexts, 'sajutoktok/search.html')


def contact(request): # Contact
    account = get_account(request)
    notifications = get_notifications(request)

    # contexts
    contexts = {
        'account': account,
        'notifications': notifications,
    }

    return ut.print_info_n_return(request, 'def contact(request): # Contact', contexts, 'sajutoktok/contact.html')

def terms(request): # Terms of Service
    return render(request, 'sajutoktok/terms.html')

def chats(request): # Chats
    account = get_account(request)
    notifications = get_notifications(request)

    if account['id'] == '':
        return redirect('login')

    # contexts
    chat_rooms = do.get_chat_rooms(account['id'])
    contexts = {
        'account': account,
        'notifications': notifications,

        'chat_rooms': chat_rooms,
    }

    return ut.print_info_n_return(request, 'def chats(request): # Chats', contexts, 'sajutoktok/chats.html')

def chat(request): # Chat
    account = get_account(request)
    notifications = get_notifications(request)

    if account['id'] == '':
        return redirect('login')

    # data
    id = request.GET.get('opponent', '') # opponent account id

    # contexts
    chats = do.get_chats(account['id'], id) # me, opponent
    if len(chats) > 0:
        last_chat = chats[len(chats) - 1]
    else:
        last_chat = {
            'dt': ut.get_full_dt(),
        }
    contexts = {
        'account': account,
        'notifications': notifications,

        'chats': chats,
        'opponent': do.get_account(id),
        'last_dt': last_chat['dt'],
    }

    return ut.print_info_n_return(request, 'def chat(request): # Chat', contexts, 'sajutoktok/chat.html')

def chat_frame(request): # Chat Frame
    account = get_account(request)
    notifications = get_notifications(request)

    if account['id'] == '':
        return redirect('login')

    # data
    id = request.GET.get('opponent', '') # opponent account id

    # contexts
    chats = do.get_chats(account['id'], id) # me, opponent
    if len(chats) > 0:
        last_chat = chats[len(chats) - 1]
    else:
        last_chat = {
            'dt': ut.get_full_dt(),
        }
    contexts = {
        'account': account,
        'notifications': notifications,

        'chats': chats,
        'opponent': do.get_account(id),
        'last_dt': last_chat['dt'],
    }

    return ut.print_info_n_return(request, 'def chat_frame(request): # Chat Frame', contexts, 'sajutoktok/chat_frame.html')



##########
# accounts
def login(request): # login
    contexts = get_default_contexts(request)
    if contexts['account'] != None:
        return redirect('/')
    return render(request, 'sajutoktok/login.html', contexts)

def register_cert_request(request): # register cert request(email)
    contexts = get_default_contexts(request)
    if contexts['account'] != None:
        return redirect('/')
    return render(request, 'sajutoktok/register_cert_request.html', contexts)

def register_cert_confirm(request): # register cert confirm
    contexts = get_default_contexts(request)
    if contexts['account'] != None:
        return redirect('/')

    # POST
    contexts['email'] = request.POST.get('email', '')
    if contexts['email'] == '':
        return redirect('register_cert_request')

    return render(request, 'sajutoktok/register_cert_confirm.html', contexts)

def register_select(request): # user register select
    account = get_account(request)
    notifications = get_notifications(request)
    if account['id'] != '': # permission
        return redirect('login')

    # data
    email = request.POST.get('email', '')
    code = request.POST.get('code', '')
    if email == '' or code == '':
        return redirect('register_cert_request')

    # contexts
    contexts = {
        'account': account,
        'notifications': notifications,

        'email': email,
        'code': code,
    }

    return render(request, 'sajutoktok/register_select.html', contexts)

def register_user(request): # user register
    account = get_account(request)
    notifications = get_notifications(request)
    if account['id'] != '': # permission
        return redirect('login')

    # data
    email = request.POST.get('email', '')
    code = request.POST.get('code', '')
    if email == '' or code == '':
        return redirect('register_cert_request')

    # contexts
    contexts = {
        'account': account,
        'notifications': notifications,

        'email': email,
        'code': code,
    }

    return render(request, 'sajutoktok/register_user.html', contexts)

def register_counselor(request): # counselor register
    account = get_account(request)
    notifications = get_notifications(request)
    if account['id'] != '': # permission
        return redirect('login')

    # data
    email = request.POST.get('email', '')
    code = request.POST.get('code', '')
    if email == '' or code == '':
        return redirect('register_cert_request')

    # contexts
    contexts = {
        'account': account,
        'notifications': notifications,

        'email': email,
        'code': code,
    }

    return render(request, 'sajutoktok/register_counselor.html', contexts)

def forgot_cert_request(request): # forgot cert request(tel)
    account = get_account(request)
    notifications = get_notifications(request)

    # contexts
    contexts = {
        'account': account,
        'notifications': notifications,
    }

    return render(request, 'sajutoktok/forgot_cert_request.html', contexts)

def forgot_cert_confirm(request): # forgot cert confirm
    account = get_account(request)
    notifications = get_notifications(request)

    # data
    email = request.POST.get('email', '')

    # contexts
    contexts = {
        'account': account,
        'notifications': notifications,

        'email': email,
    }

    return render(request, 'sajutoktok/forgot_cert_confirm.html', contexts)

def forgot_password_reset(request): # forgot password reset
    account = get_account(request)
    notifications = get_notifications(request)

    # data
    email = request.POST.get('email', '')
    code = request.POST.get('code', '')

    # contexts
    cert = mo.CERT_CODE.objects.filter(
        method=email,
        code=code,
    ).first()
    if cert is None:
        return redirect('forgot_cert_request')
    contexts = {
        'account': account,
        'notifications': notifications,

        'email': cert.method,
        'code': cert.code,
    }

    return render(request, 'sajutoktok/forgot_password_reset.html', contexts)

def profile_user(request): # user profile
    account = get_account(request)
    notifications = get_notifications(request)

    if account['id'] == '':
        return redirect('login')
    if account['account_type'] == 'counselor':
        return redirect('profile_counselor')

    # contexts
    qnas = do.get_user_qnas(account['id'])[:3]
    reviews = do.get_user_reviews(account['id'])
    purchases = do.get_user_purchases(account['id'])
    contexts = {
        'account': account,
        'notifications': notifications,

        'user': account,
        'qnas': qnas,
        'reviews': reviews,
        'purchases': purchases,
    }

    return ut.print_info_n_return(request, 'def profile_user(request): # user profile', contexts, 'sajutoktok/profile_user.html')

def profile_user_qnas(request): # user qna post list
    account = get_account(request)
    notifications = get_notifications(request)

    if account['id'] == '':
        return redirect('login')
    if account['account_type'] == 'counselor':
        return redirect('profile_counselor')

    # contexts
    qnas = do.get_user_qnas(account['id'])
    contexts = {
        'account': account,
        'notifications': notifications,

        'qnas': qnas,
    }

    return ut.print_info_n_return(request, 'def profile_user_qnas(request): # user qna post list', contexts, 'sajutoktok/profile_user_qnas.html')

def profile_user_purchases(request): # user purchases
    account = get_account(request)
    notifications = get_notifications(request)

    if account['id'] == '':
        return redirect('login')
    if account['account_type'] == 'counselor':
        return redirect('profile_counselor')

    # contexts
    purchases = do.get_user_purchases(account['id'])
    contexts = {
        'account': account,
        'notifications': notifications,

        'purchases': purchases,
    }

    return ut.print_info_n_return(request, 'def profile_user_purchases(request): # user purchases', contexts, 'sajutoktok/profile_user_purchases.html')

def profile_user_purchase_refund(request): # user purchase refund
    account = get_account(request)
    notifications = get_notifications(request)

    if account['id'] == '':
        return redirect('login')
    if account['account_type'] == 'counselor':
        return redirect('profile_counselor')

    # data
    id = request.GET.get('id', 0) # purchase id

    # contexts
    purchase = do.get_purchase(id)
    if purchase['id'] == '':
        return redirect('profile_user_purchases')
    contexts = {
        'account': account,
        'notifications': notifications,

        'purchase': purchase,
    }

    return ut.print_info_n_return(request, 'def profile_user_purchase_refund(request): # user purchase refund', contexts, 'sajutoktok/profile_user_purchase_refund.html')

def profile_user_point_shop(request): # user point shop
    account = get_account(request)
    notifications = get_notifications(request)

    if account['id'] == '':
        return redirect('login')
    if account['account_type'] == 'counselor':
        return redirect('profile_counselor')

    # contexts
    items = do.get_items('point')
    contexts = {
        'account': account,
        'notifications': notifications,

        'items': items,
    }

    return ut.print_info_n_return(request, 'def profile_user_point_shop(request): # user point shop', contexts, 'sajutoktok/profile_user_point_shop.html')

def profile_user_purchase(request): # user purchase
    account = get_account(request)
    notifications = get_notifications(request)

    if account['id'] == '':
        return redirect('login')
    if account['account_type'] == 'counselor':
        return redirect('profile_counselor')

    # data
    id = request.GET.get('id', 0) # item id

    # contexts
    item = do.get_item(id)
    if item['id'] == '':
        return redirect('index')
    contexts = {
        'account': account,
        'notifications': notifications,

        'item': item,
    }

    return ut.print_info_n_return(request, 'def profile_user_purchase(request): # user purchase', contexts, 'sajutoktok/profile_user_purchase.html')

@ csrf_exempt
def profile_user_purchase_confirm(request): # user purchase confirm
    # data
    user_id = request.POST['user_id']
    pgcode = request.POST['pgcode']
    user_name = request.POST['user_name']
    order_no = request.POST['order_no']
    service_name = request.POST['service_name']
    product_name = request.POST['product_name']
    code = request.POST['code']
    message = request.POST['message']

    account = mo.ACCOUNT.objects.filter(id=user_id).first()
    if account is None:
        return redirect('login')
    notifications = do.get_notifications(user_id)

    if account['id'] == '':
        return redirect('login')

    # contexts
    purchase = mo.PURCHASE.objects.filter(
        id = order_no,
        user_id = user_id,
    ).first()
    if purchase is None:
        return redirect('profile_user_purchase_cancel')
    purchase.status = 'completed'
    purchase.log = f'[결제 완료] {service_name} 상품의 결제가 완료되었습니다. 완료일시: {ut.get_now_dt()} 금액: {purchase.price}'
    purchase.save()
    account.point += purchase.price
    account.save()
    account = do.get_account(user_id)
    purchase = do.get_purchase(order_no)

    contexts = {
        'account': account,
        'notifications': notifications,

        'purchase': purchase,
        'item': purchase['item']
    }

    return render(request, 'sajutoktok/profile_user_purchase_confirm.html', contexts)

@ csrf_exempt
def profile_user_purchase_cancel(request): # user purchase cancel
    return render(request, 'sajutoktok/profile_user_purchase_cancel.html')

def profile_counselor(request): # counselor profile
    account = get_account(request)
    notifications = get_notifications(request)

    if account['id'] == '':
        return redirect('login')
    if account['account_type'] == 'user':
        return redirect('/')

    # data
    counselor_id = request.GET.get('id', account['id']) # counselor id

    # contexts
    qnas = do.get_counselor_qnas(counselor_id, 1)[:3]
    blogs = do.get_counselor_blogs(counselor_id, 1)[:5]
    reviews = do.get_counselor_reviews(counselor_id, 1)[:5]
    purchases = do.get_counselor_purchases(counselor_id, 1)
    items = do.get_counselor_items(counselor_id)
    contexts = {
        'account': account,
        'notifications': notifications,

        'counselor': account,
        'qnas': qnas,
        'blogs': blogs,
        'reviews': reviews,
        'purchases': purchases,
        'items': items,
    }

    return ut.print_info_n_return(request, 'def profile_counselor(request): # counselor profile', contexts, 'sajutoktok/profile_counselor.html')

def profile_counselor_qnas(request): # counselor qna post list
    account = get_account(request)
    notifications = get_notifications(request)

    if account['id'] == '':
        return redirect('login')
    if account['account_type'] == 'user':
        return redirect('profile_user')

    # contexts
    qnas = do.get_all_counselor_qnas(account['id'])
    contexts = {
        'account': account,
        'notifications': notifications,

        'qnas': qnas,
    }

    return ut.print_info_n_return(request, 'def profile_counselor_qnas(request): # counselor qna post list', contexts, 'sajutoktok/profile_counselor_qnas.html')

def profile_counselor_qna(request): # counselor qna post detail
    account = get_account(request)
    notifications = get_notifications(request)

    if account['id'] == '':
        return redirect('login')
    if account['account_type'] == 'user':
        return redirect('profile_user')

    # data
    id = request.GET.get('id', 0)

    # contexts
    qna = do.get_post(id)
    if qna['id'] == '':
        return redirect('profile_counselor_qnas')
    contexts = {
        'account': account,
        'notifications': notifications,

        'qna': qna,
    }

    return ut.print_info_n_return(request, 'def profile_counselor_qna(request): # counselor qna post detail', contexts, 'sajutoktok/profile_counselor_qna.html')

def profile_counselor_blogs(request): # counselor blog post list
    account = get_account(request)
    notifications = get_notifications(request)

    if account['id'] == '':
        return redirect('login')
    if account['account_type'] == 'user':
        return redirect('profile_user')

    # contexts
    blogs = do.get_all_counselor_blogs(account['id'])
    contexts = {
        'account': account,
        'notifications': notifications,

        'blogs': blogs,
    }

    return ut.print_info_n_return(request, 'def profile_counselor_blogs(request): # counselor blog post list', contexts, 'sajutoktok/profile_counselor_blogs.html')

def profile_counselor_blog(request): # counselor blog post detail
    account = get_account(request)
    notifications = get_notifications(request)

    if account['id'] == '':
        return redirect('login')
    if account['account_type'] == 'user':
        return redirect('profile_user')

    # data
    id = request.GET.get('id', 0) # blog id

    # contexts
    blog = do.get_post(id)
    if blog['id'] == '':
        return redirect('profile_counselor_blogs')
    contexts = {
        'account': account,
        'notifications': notifications,

        'blog': blog,
    }

    return ut.print_info_n_return(request, 'def profile_counselor_blog(request): # counselor blog post detail', contexts, 'sajutoktok/profile_counselor_blog.html')

def profile_counselor_blog_write(request): # counselor blog post write
    account = get_account(request)
    notifications = get_notifications(request)

    if account['id'] == '':
        return redirect('login')
    if account['account_type'] == 'user':
        return redirect('profile_user')

    # contexts
    contexts = {
        'account': account,
        'notifications': notifications,
    }

    return ut.print_info_n_return(request, 'def profile_counselor_blog_write(request): # counselor blog post write', contexts, 'sajutoktok/profile_counselor_blog_write.html')

def profile_counselor_purchases(request): # counselor purchase list
    account = get_account(request)
    notifications = get_notifications(request)

    if account['id'] == '':
        return redirect('login')
    if account['account_type'] == 'user':
        return redirect('profile_user')

    # contexts
    purchases = do.get_counselor_purchases(account['id'], 1)
    contexts = {
        'account': account,
        'notifications': notifications,

        'purchases': purchases,
    }

    return ut.print_info_n_return(request, 'def profile_counselor_purchases(request): # counselor purchase list', contexts, 'sajutoktok/profile_counselor_purchases.html')

def counselor(request): # counselor main
    account = get_account(request)
    notifications = get_notifications(request)

    # data
    id = request.GET.get('id', 0) # counselor id
    if id == account['id']:
        return redirect('profile_counselor')
    page = request.GET.get('page', 1) # review list page

    # contexts
    counselor = do.get_account(id)
    if counselor['id'] == '':
        return redirect('/')
    qnas = do.get_counselor_qnas(counselor['id'], 1)[:3]
    blogs = do.get_counselor_blogs(counselor['id'], 1)[:5]
    reviews = do.get_counselor_reviews(counselor['id'], page)
    review_sum = 0
    for review in reviews:
        review_sum += int(review['star'])
    try:
        review_avg = int((review_sum / len(reviews))*10)/10
    except:
        review_avg = 0
    contexts = {
        'account': account,
        'notifications': notifications,

        'counselor': counselor,
        'blogs': blogs,
        'reviews': reviews,
        'review_avg': review_avg,
        'qnas': qnas,
    }

    return ut.print_info_n_return(request, 'def counselor(request): # counselor main', contexts, 'sajutoktok/counselor.html')

def counselor_blogs(request): # counselor blog post list
    account = get_account(request)
    notifications = get_notifications(request)

    # data
    id = request.GET.get('id', 0) # counselor id
    page = request.GET.get('page', 1) # blog list page

    # contexts
    counselor = do.get_account(id)
    if counselor['id'] == '':
        return redirect('index')
    blogs = do.get_all_counselor_blogs(counselor['id'])
    contexts = {
        'account': account,
        'notifications': notifications,

        'counselor': counselor,
        'blogs': blogs,
    }

    return ut.print_info_n_return(request, 'def counselor_blogs(request): # counselor blog post list', contexts, 'sajutoktok/counselor_blogs.html')

def counselor_blog(request): # counselor blog post detail
    account = get_account(request)
    notifications = get_notifications(request)

    # data
    id = request.GET.get('id', 0) # counselor id
    blog_id = request.GET.get('blog_id', 0) # blog id

    # contexts
    counselor = do.get_account(id)
    blog = do.get_post(blog_id)
    update_post_views(request, blog) # update post views
    if blog['id'] == '':
        return redirect('counselor_blogs')
    contexts = {
        'account': account,
        'notifications': notifications,

        'counselor': counselor,
        'blog': blog,
    }

    return ut.print_info_n_return(request, 'def counselor_blog(request): # counselor blog post detail', contexts, 'sajutoktok/counselor_blog.html')

def counselor_qnas(request): # counselor qna post list
    account = get_account(request)
    notifications = get_notifications(request)

    if account['id'] == '':
        return redirect('login')

    # data
    id = request.GET.get('id', '') # counselor id

    # contexts
    counselor = do.get_account(id)
    if counselor['id'] == '':
        return redirect('index')
    qnas = do.get_counselor_qnas(counselor['id'], 'all')
    contexts = {
        'account': account,
        'notifications': notifications,

        'counselor': counselor,
        'qnas': qnas,
    }

    return ut.print_info_n_return(request, 'def counselor_qnas(request): # counselor qna post list', contexts, 'sajutoktok/counselor_qnas.html')

def counselor_qna(request): # counselor qna post detail
    account = get_account(request)
    notifications = get_notifications(request)

    if account['id'] == '':
        return redirect('login')

    # data
    id = request.GET.get('id', 0) # counselor id
    qna_id = request.GET.get('qna_id', 0) # qna id

    # contexts
    counselor = do.get_account(id)
    qna = do.get_post(qna_id)
    if qna['id'] == '':
        return redirect('counselor_qnas')
    contexts = {
        'account': account,
        'notifications': notifications,

        'counselor': counselor,
        'qna': qna,
    }

    return ut.print_info_n_return(request, 'def counselor_qna(request): # counselor qna post detail', contexts, 'sajutoktok/counselor_qna.html')

def counselor_qna_write(request): # counselor qna post write
    account = get_account(request)
    notifications = get_notifications(request)

    if account['id'] == '':
        return redirect('login')

    # data
    id = request.GET.get('id', 0) # counselor id

    # contexts
    counselor = do.get_account(id)
    contexts = {
        'account': account,
        'notifications': notifications,

        'counselor': counselor,
    }

    return ut.print_info_n_return(request, 'def counselor_qna_write(request): # counselor qna post write', contexts, 'sajutoktok/counselor_qna_write.html')



##########
# supervisor
def supervisor(request): # supervisor main
    account = get_account(request)
    notifications = get_notifications(request)

    if account['account_type'] != 'supervisor':
        return redirect('supervisor_login')

    # contexts
    contexts = {
        'account': account,
        'notifications': notifications,
    }

    return render(request, 'sajutoktok/supervisor.html', contexts)

def supervisor_login(request): # supervisor login
    account = get_account(request)

    if account['account_type'] == 'supervisor':
        return redirect('supervisor')

    # contexts
    contexts = {
        'account': account,
        'ip': ut.get_ip(request),
    }

    return render(request, 'sajutoktok/supervisor_login.html', contexts)

def supervisor_notices(request): # supervisor notice post list
    account = get_account(request)
    notifications = get_notifications(request)

    if account['account_type'] != 'supervisor':
        return redirect('supervisor_login')

    # contexts
    notices = do.get_all_notices()
    contexts = {
        'account': account,
        'notifications': notifications,

        'notices': notices,
    }

    return render(request, 'sajutoktok/supervisor_notices.html', contexts)

def supervisor_notice(request): # supervisor notice post detail
    account = get_account(request)
    notifications = get_notifications(request)

    if account['account_type'] != 'supervisor':
        return redirect('supervisor_login')

    # data
    id = request.GET.get('id', 0) # notice id

    # contexts
    notice = do.get_post(id)
    if notice['id'] == '':
        return redirect('supervisor_notices')
    contexts = {
        'account': account,
        'notifications': notifications,

        'notice': notice,
    }

    return render(request, 'sajutoktok/supervisor_notice.html', contexts)

def supervisor_notice_write(request): # supervisor notice post write
    account = get_account(request)
    notifications = get_notifications(request)

    if account['account_type'] != 'supervisor':
        return redirect('supervisor_login')

    # contexts
    contexts = {
        'account': account,
        'notifications': notifications,
    }

    return render(request, 'sajutoktok/supervisor_notice_write.html', contexts)

def supervisor_events(request): # supervisor event post list
    account = get_account(request)
    notifications = get_notifications(request)

    if account['account_type'] != 'supervisor':
        return redirect('supervisor_login')

    # contexts
    events = do.get_all_events()
    contexts = {
        'account': account,
        'notifications': notifications,

        'events': events,
    }

    return ut.print_info_n_return(request, 'def supervisor_events(request): # supervisor event post list', contexts, 'sajutoktok/supervisor_events.html')

def supervisor_event(request): # supervisor event post detail
    account = get_account(request)
    notifications = get_notifications(request)

    if account['account_type'] != 'supervisor':
        return redirect('supervisor_login')

    # data
    id = request.GET.get('id', 0) # event id

    # contexts
    event = do.get_post(id)
    if event['id'] == '':
        return redirect('supervisor_events')
    contexts = {
        'account': account,
        'notifications': notifications,

        'event': event,
    }

    return ut.print_info_n_return(request, 'def supervisor_event(request): # supervisor event post detail', contexts, 'sajutoktok/supervisor_event.html')

def supervisor_event_write(request): # supervisor event post write
    account = get_account(request)
    notifications = get_notifications(request)

    if account['account_type'] != 'supervisor':
        return redirect('supervisor_login')

    # contexts
    contexts = {
        'account': account,
        'notifications': notifications,
    }

    return render(request, 'sajutoktok/supervisor_event_write.html', contexts)

def supervisor_counselors(request): # supervisor counselor list
    account = get_account(request)
    notifications = get_notifications(request)

    if account['account_type'] != 'supervisor':
        return redirect('supervisor_login')

    # contexts
    counselors = do.get_all_counselors()

    contexts = {
        'account': account,
        'notifications': notifications,

        'counselors': counselors,
    }

    return render(request, 'sajutoktok/supervisor_counselors.html', contexts)

def supervisor_counselor(request): # supervisor counselor detail
    account = get_account(request)
    notifications = get_notifications(request)

    if account['account_type'] != 'supervisor':
        return redirect('supervisor_login')

    # data
    id = request.GET.get('id', 0) # counselor id
    page = int(request.GET.get('page', 1)) # review list page

    # contexts
    counselor = do.get_account(id)
    qnas = do.get_counselor_qnas(counselor['id'], 1)[:3]
    blogs = do.get_counselor_blogs(counselor['id'], 1)[:5]
    reviews = do.get_counselor_reviews(counselor['id'], page)
    review_sum = 0
    for review in reviews:
        review_sum += int(review['star'])
    try:
        review_avg = int((review_sum / len(reviews))*10)/10
    except:
        review_avg = 0
    if counselor['id'] == '':
        return redirect('supervisor_counselors')
    purchases = do.get_counselor_purchases(counselor['id'], 1)
    items = do.get_counselor_items(counselor['id'])
    contexts = {
        'account': account,
        'notifications': notifications,

        'counselor': counselor,
        'qnas': qnas,
        'blogs': blogs,
        'reviews': reviews,
        'review_avg': review_avg,
        'purchases': purchases,
        'items': items,
    }

    return ut.print_info_n_return(request, 'def supervisor_counselor(request): # supervisor counselor detail', contexts, 'sajutoktok/supervisor_counselor.html')

def supervisor_users(request): # supervisor user list
    account = get_account(request)
    notifications = get_notifications(request)

    if account['account_type'] != 'supervisor':
        return redirect('supervisor_login')

    # contexts
    users = do.get_all_users()
    contexts = {
        'account': account,
        'notifications': notifications,

        'users': users,
    }

    return render(request, 'sajutoktok/supervisor_users.html', contexts)

def supervisor_user(request): # supervisor user detail
    account = get_account(request)
    notifications = get_notifications(request)

    if account['account_type'] != 'supervisor':
        return redirect('supervisor_login')

    # data
    id = request.GET.get('id', 0) # user id

    # contexts
    user = do.get_account(id)
    if user['id'] == '':
        return redirect('supervisor_users')
    qnas = do.get_user_qnas(user['id'])
    reviews = do.get_user_reviews(user['id'])
    purchases = do.get_user_purchases(user['id'])
    contexts = {
        'account': account,
        'notifications': notifications,

        'user': user,
        'qnas': qnas,
        'reviews': reviews,
        'purchases': purchases,
    }

    return render(request, 'sajutoktok/supervisor_user.html', contexts)

# 상품리스트 페이지
# 모든 상품 로드, 상품 추가 버튼
def supervisor_items(request):
    account = get_account(request)
    notifications = get_notifications(request)

    if account['account_type'] != 'supervisor':
        return redirect('supervisor_login')

    # contexts
    items = do.get_market_items()
    contexts = {
        'account': account,
        'notifications': notifications,

        'items': items,
    }

    return render(request, 'sajutoktok/supervisor_items.html', contexts)

# 상품 페이지
# 해당 상품 로드. 상품 수정 가능. GET: id
def supervisor_item(request):
    account = get_account(request)
    notifications = get_notifications(request)

    if account['account_type'] != 'supervisor':
        return redirect('supervisor_login')

    # data
    id = request.GET.get('id', 0)

    # contexts
    item = do.get_item(id)
    if item['id'] == '':
        return redirect('supervisor_items')
    contexts = {
        'account': account,
        'notifications': notifications,

        'item': item,
    }

    return render(request, 'sajutoktok/supervisor_item.html', contexts)

# 결제 내역 리스트 페이지
# 모든 결제 내역 로드
def supervisor_purchases(request):
    account = get_account(request)
    notifications = get_notifications(request)

    if account['account_type'] != 'supervisor':
        return redirect('supervisor_login')

    # contexts
    purchases = do.get_all_purchases()
    contexts = {
        'account': account,
        'notifications': notifications,

        'purchases': purchases,
    }

    return render(request, 'sajutoktok/supervisor_purchases.html', contexts)

def supervisor_send_push(request): # supervisor send push
    account = get_account(request)
    notifications = get_notifications(request)

    if account['account_type'] != 'supervisor':
        return redirect('supervisor_login')

    # contexts
    contexts = {
        'account': account,
        'notifications': notifications,
    }

    return render(request, 'sajutoktok/supervisor_send_push.html', contexts)

##########
# callbacks
@ csrf_exempt
def callback_purchase(request): # purchase callback
    gets = request.GET
    posts = request.POST

    # print data
    print('callback_purchase')
    print('gets:', gets)
    print('posts:', posts)

    return HttpResponse('callback_purchase')

