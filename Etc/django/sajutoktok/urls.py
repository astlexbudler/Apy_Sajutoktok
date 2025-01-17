from django.urls import path
from . import views as v
from . import apis as a
from . import orms as o



urlpatterns = [

    # v.py
    # 시작 페이지
    # 전화상담, 채팅상담, 대면상담, 카페상담, 점사마켓, 공지사항, 이벤트, 리뷰, 포인트 상점 메뉴 구성
    path('', v.index, name='index'),
    # 공지사항 리스트 페이지
    # 모든 공지사항 로드
    path('notices', v.notices, name='notices'),
    # 공지사항 페이지
    # 해당 공지사항 로드 GET: id
    path('notice', v.notice, name='notice'),
    # 이벤트 리스트 페이지
    # 모든 이벤트 로드
    path('events', v.events, name='events'),
    # 이벤트 페이지
    # 해당 이벤트 로드 GET: id
    path('event', v.event, name='event'),
    # 모든 리뷰 리스트 페이지
    # 리뷰 리스트 로드 POST: page(infinite scroll)
    path('all_reviews', v.all_reviews, name='all_reviews'),
    # 포인트 상점 페이지
    # 포인트 구매 아이템 로드. 사용자 계정만 접근 가능
    path('point_shop', v.point_shop, name='point_shop'),
    # 포인트 결제 페이지
    # 포인트 구매 아이템 결제 GET: id
    path('point_shop_purchase', v.point_shop_purchase, name='point_shop_purchase'),
    # 결제 완료 페이지
    path('point_shop_purchase_confirm', v.point_shop_purchase_confirm, name='point_shop_purchase_confirm'),
    # 결제 취소 페이지
    path('point_shop_purchase_cancel', v.point_shop_purchase_cancel, name='point_shop_purchase_cancel'),
    # 결제 콜백 처리 주소
    path('purchase_callback', v.purchase_callback, name='purchase_callback'),
    # 영수증 페이지
    # 영수증 로드 GET: id
    path('purchase_detail', v.purchase_detail, name='purchase_detail'),
    # 서비스 관리자 페이지
    # 서비스 관리자 이름 및 연락처
    path('contact', v.contact, name='contact'),
    # 이용약관 페이지
    # 이용약관 내용
    path('terms', v.terms, name='terms'),
    # 검색 페이지
    # 상담가 검색 페이지 GET: category, service, keyword POST: page
    path('search', v.search, name='search'),
    # 상담가 페이지
    # 상담가 정보 페이지 GET: id
    path('counselor', v.counselor, name='counselor'),
    # 로그인 페이지
    # 로그인 페이지, SNS 로그인 버튼
    path('login', v.login, name='login'),
    # SNS 로그인 콜백 페이지
    # 카카오톡
    #path('login_kakao', v.login_kakao, name='login_kakao'),
    # 네이버
    #path('login_naver', v.login_naver, name='login_naver'),
    # 애플
    #path('login_apple', v.login_apple, name='login_apple'),
    # 회원가입 이메일 인증 페이지
    # 회원가입 이메일 인증 페이지
    path('register_cert_request', v.register_cert_request, name='register_cert_request'),
    # 회원가입 이메일 인증 확인 페이지
    # 회원가입 이메일 인증 확인 페이지
    path('register_cert_confirm', v.register_cert_confirm, name='register_cert_confirm'),
    # 회원가입 회원 선택 페이지
    # 회원가입 회원 선택 페이지, 사용자, 상담사 선택
    path('register_select', v.register_select, name='register_select'),
    # 사용자 회원가입 페이지
    # 사용자 회원가입 페이지. ID, PW, 닉네임, 연락처 입력
    path('register_user', v.register_user, name='register_user'),
    # 상담사 회원가입 페이지
    # 상담사 회원가입 페이지. 이름, 이메일, 연락처 입력(가입 요청 이메일 발송)
    path('register_counselor', v.register_counselor, name='register_counselor'),
    # 회원 찾기 이메일 인증 페이지
    # 회원 찾기 이메일 인증 페이지
    path('forgot_cert_request', v.forgot_cert_request, name='forgot_cert_request'),
    # 회원 찾기 이메일 인증 확인 페이지
    # 이메일 인증번호 입력 페이지
    path('forgot_cert_confirm', v.forgot_cert_confirm, name='forgot_cert_confirm'),
    # 회원 찾기 비밀번호 재설정 페이지
    # 비밀번호 재설정 페이지
    path('forgot_password_reset', v.forgot_password_reset, name='forgot_password_reset'),
    # 상담가 프로필 페이지
    # 상담가 프로필 페이지 GET: id(없을 경우 로그인한 상담가 정보 또는 redirect)
    path('profile_counselor', v.profile_counselor, name='profile_counselor'),
    # 상담가 블로그 리스트 페이지
    # 상담가 블로그 리스트 페이지 GET: id(상담가 id)
    path('counselor_blogs', v.counselor_blogs, name='counselor_blogs'),
    # 상담가 블로그 게시글 작성 페이지
    # 상담가 블로그 게시글 작성 페이지 GET: id(상담가 id)
    path('profile_counselor_blog_write', v.profile_counselor_blog_write, name='profile_counselor_blog_write'),
    # 상담가 블로그 페이지
    # 상담가 블로그 페이지 GET: id(블로그 id)
    path('counselor_blog', v.counselor_blog, name='counselor_blog'),
    # 상담가 QnA 리스트 페이지
    # 상담가 QnA 리스트 페이지 GET: id(상담가 id)
    path('counselor_qnas', v.counselor_qnas, name='counselor_qnas'),
    # 채팅 페이지
    # 채팅 페이지 GET: opponent(상담가 id)
    path('chat', v.chat, name='chat'),

    # accounts
    path('profile_user', v.profile_user, name='profile_user'), # user profile
    path('profile_user_qnas', v.profile_user_qnas, name='profile_user_qnas'), # user qna post list
    path('profile_user_purchases', v.profile_user_purchases, name='profile_user_purchases'), # user purchases
    path('profile_user_purchase_refund', v.profile_user_purchase_refund, name='profile_user_purchase_refund'), # user purchase refund
    path('profile_user_point_shop', v.profile_user_point_shop, name='profile_user_point_shop'), # user point shop
    path('profile_user_purchase', v.profile_user_purchase, name='profile_user_purchase'), # user purchase
    path('profile_user_purchase_confirm', v.profile_user_purchase_confirm, name='profile_user_purchase_confirm'), # user purchase confirm
    path('profile_user_purchase_cancel', v.profile_user_purchase_cancel, name='profile_user_purchase_cancel'), # user purchase cancel
    # counselor
    path('profile_counselor', v.profile_counselor, name='profile_counselor'), # counselor profile
    path('profile_counselor_qnas', v.profile_counselor_qnas, name='profile_counselor_qnas'), # counselor qna post list
    path('profile_counselor_qna', v.profile_counselor_qna, name='profile_counselor_qna'), # counselor qna post detail
    path('profile_counselor_blogs', v.profile_counselor_blogs, name='profile_counselor_blogs'), # counselor blog post list
    path('profile_counselor_blog', v.profile_counselor_blog, name='profile_counselor_blog'), # counselor blog post detail
    path('profile_counselor_blog_write', v.profile_counselor_blog_write, name='profile_counselor_blog_write'), # counselor blog post write
    path('profile_counselor_purchases', v.profile_counselor_purchases, name='profile_counselor_purchases'), # counselor purchase list
    
    
    path('counselor_blog', v.counselor_blog, name='counselor_blog'), # counselor blog post detail
    path('counselor_qnas', v.counselor_qnas, name='counselor_qnas'), # counselor qna post list
    path('counselor_qna', v.counselor_qna, name='counselor_qna'), # counselor qna post detail
    path('counselor_qna_write', v.counselor_qna_write, name='counselor_qna_write'), # counselor qna post write\
    # supervisor
    # 관리자 로그인 페이지
    # 관리자 로그인
    path('supervisor_login', v.supervisor_login, name='supervisor_login'),
    # 관리자 페이지 메인
    # 공지사항, 이벤트, 상담사, 사용자, 구매내역, 푸시 발송 메뉴 구성
    path('supervisor', v.supervisor, name='supervisor'),
    # 공지사항 리스트 페이지
    # 모든 공지사항 로드
    path('supervisor_notices', v.supervisor_notices, name='supervisor_notices'),
    # 공지사항 페이지
    # 해당 공지사항 로드. 공지사항 내용 수정 가능. GET: id
    path('supervisor_notice', v.supervisor_notice, name='supervisor_notice'),
    # 공지사항 작성 페이지
    # 공지사항 작성
    path('supervisor_notice_write', v.supervisor_notice_write, name='supervisor_notice_write'), # supervisor notice post write
    # 이벤트 리스트 페이지
    # 모든 이벤트 로드
    path('supervisor_events', v.supervisor_events, name='supervisor_events'),
    # 이벤트 페이지
    # 해당 이벤트 로드. 이벤트 내용 수정 가능. GET: id
    path('supervisor_event', v.supervisor_event, name='supervisor_event'),
    # 이벤트 작성 페이지
    # 이벤트 작성
    path('supervisor_event_write', v.supervisor_event_write, name='supervisor_event_write'),
    # 상담사 계정 리스트 페이지
    # 모든 상담사 계정 로드. 상담가 동기화 버튼.
    path('supervisor_counselors', v.supervisor_counselors, name='supervisor_counselors'),
    # 상담사 계정 페이지
    # 해당 상담사 계정 로드. 상담사 계정 수정 가능. GET: id
    path('supervisor_counselor', v.supervisor_counselor, name='supervisor_counselor'),
    # 사용자 계정 리스트 페이지
    # 모든 사용자 계정 로드
    path('supervisor_users', v.supervisor_users, name='supervisor_users'),
    # 사용자 계정 페이지
    # 해당 사용자 계정 로드. 사용자 계정 수정 가능. GET: id
    path('supervisor_user', v.supervisor_user, name='supervisor_user'),
    # 상품리스트 페이지
    # 모든 상품 로드, 상품 추가 버튼
    path('supervisor_items', v.supervisor_items, name='supervisor_items'),
    # 상품 페이지
    # 해당 상품 로드. 상품 수정 가능. GET: id
    path('supervisor_item', v.supervisor_item, name='supervisor_item'),
    # 결제 내역 리스트 페이지
    # 모든 결제 내역 로드
    path('supervisor_purchases', v.supervisor_purchases, name='supervisor_purchases'),
    # 푸시 발송 페이지
    # 푸시 발송
    path('supervisor_send_push', v.supervisor_send_push, name='supervisor_send_push'), # supervisor send push
    # callback
    path('callback/purchase', v.callback_purchase, name='callback_purchase'), # purchase callback

    # apis
    path('api/test', a.test, name='test'), # test API
    path('api/login_account', a.login_account, name='login_account'), # try login API
    path('api/login_supervisor', a.login_supervisor, name='login_supervisor'), # try supervisor login API
    path('api/logout', a.logout_account, name='logout_account'), # logout API
    path('api/check_id', a.check_id, name='check_id'), # email duplication check API
    path('api/check_nickname', a.check_nickname, name='check_nickname'), # nickname duplication check API
    path('api/check_tel', a.check_tel, name='check_tel'), # tel duplication check API
    path('api/request_cert_code', a.request_cert_code, name='request_cert_code'), # request cert code API
    path('api/check_cert_code', a.check_cert_code, name='check_cert_code'), # check cert code API
    path('api/write_supervisor', a.write_supervisor, name='write_supervisor'), # write supervisor API
    path('api/write_account', a.write_account, name='write_account'), # write account API
    path('api/request_counselor_register', a.request_counselor_register, name='request_counselor_register'), # request counselor register API
    path('api/rewrite_account', a.rewrite_account, name='rewrite_account'), # rewrite account API
    path('api/delete_user', a.delete_user, name='delete_user'), # delete account API
    path('api/rewrite_password', a.rewrite_password, name='rewrite_password'), # rewrite password API
    path('api/set_counselor_status', a.set_counselor_status, name='set_counselor_status'), # set counselor status API
    path('api/delete_counselor', a.delete_counselor, name='delete_counselor'), # delete counselor API
    path('api/toggle_bookmark', a.toggle_bookmark, name='toggle_bookmark'), # toggle bookmark API
    path('api/add_like', a.add_like, name='add_like'), # add like API
    path('api/dislike', a.dislike, name='dislike'), # dislike API
    path('api/write_review', a.write_review, name='write_review'), # write review API
    # messaging API
    path('api/send_apppush', a.send_apppush, name='send_apppush'), # send app push API
    path('api/send_webpush', a.send_webpush, name='send_webpush'), # send web push API
    path('api/send_email', a.send_email, name='send_email'), # send email API
    path('api/send_chat', a.send_chat, name='send_chat'), # send chat API
    path('api/check_new_chat', a.check_new_chat, name='check_new_chat'), # check account new chat API
    # purchase API
    path('api/purchase_service', a.purchase_service, name='purchase_service'), # purchase item API
    path('api/refund_purchase', a.refund_purchase, name='refund_purchase'), # refund purchase API
    # CP(060) API
    path('cp/cp_sync_counselors', a.cp_sync_counselors, name='cp_sync_counselors'), # sync counselors(CP) API
    path('cp/cp_check_user', a.cp_check_user, name='cp_check_user'), # check tel(CP) API
    path('cp/cp_write_user', a.cp_write_user, name='cp_write_user'), # write user(CP) API
    path('cp/cp_check_account', a.cp_check_account, name='cp_check_account'), # check account(CP) API
    path('cp/cp_get_counselors_status', a.cp_get_counselors_status, name='cp_get_counselors_status'), # get counselors status(CP) API
    path('cp/cp_get_recent_talks', a.cp_get_recent_talks, name='cp_get_recent_talks'), # get recent talks(CP) API
    path('cp/cp_set_counselor_status', a.cp_set_counselor_status, name='cp_set_counselor_status'), # set counselor status(CP) API
    path('cp/cp_charge_point', a.cp_charge_point, name='cp_charge_point'), # charge point(CP) API
    path('cp/cp_refund_point', a.cp_refund_point, name='cp_refund_point'), # refund point(CP) API
    path('cp/cp_change_tel', a.cp_change_tel, name='cp_change_tel'), # change tel(CP) API
    path('cp/cp_change_password', a.cp_change_password, name='cp_change_password'), # change password(CP) API
    path('cp/cp_get_counselors_weights', a.cp_get_counselors_weights, name='cp_get_counselors_weights'), # get counselors weights(CP) API
    # PL(payletter) API
    path('pl/pl_request_purchase', a.pl_request_purchase, name='pl_request_purchase'), # request purchase payletter API
    path('pl/pl_confirm_subscribe', a.pl_confirm_subscribe, name='pl_confirm_subscribe'), # confirm subscribe payletter API
    path('pl/pl_cancel_purchase', a.pl_cancel_purchase, name='pl_cancel_purchase'), # cancel purchase payletter API
    path('pl/pl_partial_cancel_purchase', a.pl_partial_cancel_purchase, name='pl_partial_cancel_purchase'), # partial cancel purchase payletter API
    path('pl/pl_purchase_log', a.pl_purchase_log, name='pl_purchase_log'), # purchase log payletter API
    path('pl/pl_write_cash_receipt', a.pl_write_cash_receipt, name='pl_write_cash_receipt'), # write cash receipt payletter API
    path('pl/pl_purchase_status', a.pl_purchase_status, name='pl_purchase_status'), # purchase status payletter API
    path('pl/pl_get_receipt', a.pl_get_receipt, name='pl_get_receipt'), # get receipt payletter API

    # o.py
    path('orm/data', o.data, name='data'), # get/set/delete data RESTFUL API
    path('orm/upload_file', o.upload_file, name='upload_file'), # upload file and return file path API

]