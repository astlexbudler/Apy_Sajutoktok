from django.apps import AppConfig
from django.conf import settings

class SajutoktokConfig(AppConfig):
  default_auto_field = 'django.db.models.BigAutoField'
  name = 'sajutoktok'

  # apscheduler
  def ready(self):
    if settings.SCHEDULER_DEFAULT:
      from . import scheduler
      scheduler.startScheduler()

    try:
      # 초기 데이터 구성
      import json
      from . import models as mo
      from django.contrib.auth.models import User, Group
      from django.contrib.auth import get_user_model, authenticate, login, update_session_auth_hash, logout
      User = get_user_model()
      sajutoktok_prefix = 'sajutoktok_'

      # 앱 그룹 생성
      if not Group.objects.filter(name='sajutoktok').exists():
        Group.objects.create(name='sajutoktok')
      sajutoktok_group = Group.objects.get(name='sajutoktok')

      # 관리자 계정 생성
      if not User.objects.filter(username=f"{sajutoktok_prefix}admin").exists():
        superuser = User.objects.create_superuser(
          username=f"{sajutoktok_prefix}admin",
          password='123456a',
          first_name='관리자', # 사용자 실명
          last_name='사주톡톡', # 사용자 닉네임
          email='admin', # 이메일
          is_active=True, # 활성화 여부
          is_staff=True, # 스태프 권한
          is_superuser=True, # 슈퍼유저 권한
          user_data=json.dumps({
            'device_token': '', # 앱에서 푸시 메세지 발송을 위한 디바이스 토큰
            'push_allow': 'n', # 푸시 알림 허용 여부
            'ad_allow': 'n', # 광고 알림 허용 여부
            'type': 'supervisor', # 계정 타입
            'account_status': 'active', # 계정 상태
            'counselor_categories': '', # 상담사 사주 카테고리
            'counselor_services': '', # 상담사 제공 가능 서비스
            'online_auto_schedule_time': '', # 상담사 자동 스케줄링 시간. 설정 시 해당 시간에 상담사 상태를 자동으로 online으로 변경.
            'online_auto_schedule_toggle': 'n', # 상담사 자동 스케줄링 사용 여부
            'offline_auto_schedule_time': '', # 상담사 자동 스케줄링 시간. 설정 시 해당 시간에 상담사 상태를 자동으로 offline로 변경.
            'offline_auto_schedule_toggle': 'n', # 상담사 자동 스케줄링 사용 여부
            'online_status': '', # 상담가 온라인 상태
            'point': '0', # 보유 포인트(사용자: 사용 가능한 포인트, 상담사: 정산 가능한 포인트, 관리자: 정산된 누적 총 포인트)
            'tel': '01072729400', # 전화번호
            'address': '', # 주소
            'weight': '0', # 상담사 검색 가중치
            'profile_image_path': '', # 프로필 이미지 경로
            'introduce': '', # 상담사 소개
            'detail': '', # 상세 정보
            'like_users': '', # 상담사 좋아요
            'supervisor_note': '', # 관리자 메모
          })
        )
        sajutoktok_group.user_set.add(superuser)

      # 서버 재부팅 로그 생성
      log = mo.LOG(
        log='서버가 재부팅 되었습니다.'
      )
      log.save()

      # cert_code 테이블 초기화
      mo.CERT_CODE.objects.all().delete()

      # server_setting 테이블 초기화
      if not mo.SERVER_SETTING.objects.filter(key='060_CP_코드').exists():
        server_setting = mo.SERVER_SETTING(
          key='060_CP_코드',
          value='133'
        )
        server_setting.save()
      if not mo.SERVER_SETTING.objects.filter(key='060_서비스_번호').exists():
        server_setting = mo.SERVER_SETTING(
          key='060_서비스_번호',
          value='3005955'
        )
        server_setting.save()
      if not mo.SERVER_SETTING.objects.filter(key='SMTP_이메일_아이디').exists():
        server_setting = mo.SERVER_SETTING(
          key='SMTP_이메일_아이디',
          value='master@applifyids.com'
        )
        server_setting.save()
      if not mo.SERVER_SETTING.objects.filter(key='SMTP_이메일_비밀번호').exists():
        server_setting = mo.SERVER_SETTING(
          key='SMTP_이메일_비밀번호',
          value='applify123'
        )
        server_setting.save()
      if not mo.SERVER_SETTING.objects.filter(key='SMTP_서버_주소').exists():
        server_setting = mo.SERVER_SETTING(
          key='SMTP_서버_주소',
          value='smtp.cafe24.com'
        )
        server_setting.save()
      if not mo.SERVER_SETTING.objects.filter(key='SMTP_서버_포트').exists():
        server_setting = mo.SERVER_SETTING(
          key='SMTP_서버_포트',
          value='587'
        )
        server_setting.save()
      if not mo.SERVER_SETTING.objects.filter(key='SMTP_발송자_이름(en_only)').exists():
        server_setting = mo.SERVER_SETTING(
          key='SMTP_발송자_이름(영어)',
          value='SajuTokTok'
        )
        server_setting.save()
      if not mo.SERVER_SETTING.objects.filter(key='서비스_이름').exists():
        server_setting = mo.SERVER_SETTING(
          key='서비스_이름',
          value='사주톡톡'
        )
        server_setting.save()
      if not mo.SERVER_SETTING.objects.filter(key='서비스_로고').exists():
        server_setting = mo.SERVER_SETTING(
          key='서비스_로고',
          value='https://sajutoktok.com/static/logo.png'
        )
        server_setting.save()
      if not mo.SERVER_SETTING.objects.filter(key='회사_주소').exists():
        server_setting = mo.SERVER_SETTING(
          key='회사_주소',
          value='서울특별시 강남구 역삼동 123-456'
        )
        server_setting.save()
      if not mo.SERVER_SETTING.objects.filter(key='회사_전화번호').exists():
        server_setting = mo.SERVER_SETTING(
          key='회사_전화번호',
          value='02-1234-5678'
        )
        server_setting.save()
      if not mo.SERVER_SETTING.objects.filter(key='회사_이메일').exists():
        server_setting = mo.SERVER_SETTING(
          key='회사_이메일',
          value='company@email.com'
        )
        server_setting.save()
      if not mo.SERVER_SETTING.objects.filter(key='회사_대표자_이름').exists():
        server_setting = mo.SERVER_SETTING(
          key='회사_이름',
          value='사업자명'
        )
        server_setting.save()
      if not mo.SERVER_SETTING.objects.filter(key='개인정보_처리방침_및_이용약관').exists():
        server_setting = mo.SERVER_SETTING(
          key='개인정보_처리방침_및_이용약관',
          value='test_here'
        )
        server_setting.save()
      if not mo.SERVER_SETTING.objects.filter(key='포인트_상품_1').exists():
        server_setting = mo.SERVER_SETTING(
          key='포인트_상품_1',
          value=json.dumps({
            'name': '10,000 + 100 포인트',
            'price': '10000',
            'reward': '10100',
            'description': '사주톡톡에서 사용하는 포인트를 충전합니다. (10,000원)'
          })
        )
        server_setting.save()
      if not mo.SERVER_SETTING.objects.filter(key='포인트_상품_2').exists():
        server_setting = mo.SERVER_SETTING(
          key='포인트_상품_2',
          value=json.dumps({
            'name': '30,000 + 500 포인트',
            'price': '30000',
            'reward': '30500',
            'description': '사주톡톡에서 사용하는 포인트를 충전합니다. (30,000원)'
          })
        )
        server_setting.save()
      if not mo.SERVER_SETTING.objects.filter(key='포인트_상품_3').exists():
        server_setting = mo.SERVER_SETTING(
          key='포인트_상품_3',
          value=json.dumps({
            'name': '50,000 + 1,000 포인트',
            'price': '50000',
            'reward': '51000',
            'description': '사주톡톡에서 사용하는 포인트를 충전합니다. (50,000원)'
          })
        )
        server_setting.save()
      if not mo.SERVER_SETTING.objects.filter(key='포인트_상품_4').exists():
        server_setting = mo.SERVER_SETTING(
          key='포인트_상품_4',
          value=json.dumps({
            'name': '100,000 + 3,000 포인트',
            'price': '100000',
            'reward': '103000',
            'description': '사주톡톡에서 사용하는 포인트를 충전합니다. (100,000원)'
          })
        )
        server_setting.save()
      if not mo.SERVER_SETTING.objects.filter(key='가입_시_제공_포인트').exists():
        server_setting = mo.SERVER_SETTING(
          key='가입_시_제공_포인트',
          value='1000'
        )
        server_setting.save()
      if not mo.SERVER_SETTING.objects.filter(key='리뷰_작성_제공_포인트').exists():
        server_setting = mo.SERVER_SETTING(
          key='리뷰_작성_제공_포인트',
          value='500'
        )
        server_setting.save()
      if not mo.SERVER_SETTING.objects.filter(key='vip1_누적_포인트_기준').exists():
        server_setting = mo.SERVER_SETTING(
          key='vip1_누적_포인트_기준',
          value='100000'
        )
        server_setting.save()
      if not mo.SERVER_SETTING.objects.filter(key='vip1_충전_보너스').exists():
        server_setting = mo.SERVER_SETTING(
          key='vip1_충전_보너스',
          value='0.05'
        )
        server_setting.save()
      if not mo.SERVER_SETTING.objects.filter(key='vip2_누적_포인트_기준').exists():
        server_setting = mo.SERVER_SETTING(
          key='vip2_누적_포인트_기준',
          value='300000'
        )
        server_setting.save()
      if not mo.SERVER_SETTING.objects.filter(key='vip2_충전_보너스').exists():
        server_setting = mo.SERVER_SETTING(
          key='vip2_충전_보너스',
          value='0.1'
        )
        server_setting.save()
      if not mo.SERVER_SETTING.objects.filter(key='vip3_누적_포인트_기준').exists():
        server_setting = mo.SERVER_SETTING(
          key='vip3_누적_포인트_기준',
          value='500000'
        )
        server_setting.save()
      if not mo.SERVER_SETTING.objects.filter(key='vip3_충전_보너스').exists():
        server_setting = mo.SERVER_SETTING(
          key='vip3_충전_보너스',
          value='0.2'
        )
        server_setting.save()
      if not mo.SERVER_SETTING.objects.filter(key='상담가_포인트_정산_수수료').exists():
        server_setting = mo.SERVER_SETTING(
          key='상담가_포인트_정산_수수료',
          value='0.3'
        )
        server_setting.save()
      if not mo.SERVER_SETTING.objects.filter(key='상담가_포인트_정산일').exists():
        server_setting = mo.SERVER_SETTING(
          key='상담가_포인트_정산일',
          value='매월 1일'
        )
        server_setting.save()
      if not mo.SERVER_SETTING.objects.filter(key='상담가_포인트_최소_정산_포인트').exists():
        server_setting = mo.SERVER_SETTING(
          key='상담가_포인트_최소_정산_포인트',
          value='10000'
        )
        server_setting.save()

      # 알림 메세지
      if mo.NOTIFICATION.objects.all().count() < 5:
        for i in range(5):
          notification = mo.NOTIFICATION(
            title=f'알림 메세지 {i+1}',
            content=f'알림 메세지 {i+1} 내용입니다.',
          )
          notification.save()

      # 더미 사용자 계정 생성
      if not User.objects.filter(username=f"{sajutoktok_prefix}user@email.com").exists():
        user = User.objects.create_user(
          username=f"{sajutoktok_prefix}user@email.com",
          password='123456a',
          first_name='사용자', # 사용자 실명
          last_name='테스트 사용자', # 사용자 닉네임
          email='user@email.com',
          user_data=json.dumps({
            'device_token': '123', # 앱에서 푸시 메세지 발송을 위한 디바이스 토큰
            'push_allow': 'y', # 푸시 알림 허용 여부
            'ad_allow': 'y', # 광고 알림 허용 여부
            'type': 'user', # 계정 타입
            'account_status': 'active', # 계정 상태
            'point': '1000', # 보유 포인트(사용자: 사용 가능한 포인트, 상담사: 정산 가능한 포인트, 관리자: 정산된 누적 총 포인트)
            'tel': '01012345678', # 전화번호
            'address': '', # 주소
            'weight': '0', # 상담사 검색 가중치
            'profile_image_path': '', # 프로필 이미지 경로
            'introduce': '', # 상담사 소개
            'detail': '', # 상세 정보
            'like_counselors': '', # 사용자 좋아요
            'point_history': '', # 포인트 사용 내역
            'review_history': '', # 리뷰 내역
            'chat_history': '', # 채팅 내역
            'purchase_history': '', # 구매 내역
          })
        )
        user.groups.add(sajutoktok_group)
      else:
        user = User.objects.get(username=f"{sajutoktok_prefix}user@email.com")

      # 더미 상담사 계정 생성
      if not User.objects.filter(username=f"{sajutoktok_prefix}counselor@email.com").exists():
        counselor = User.objects.create_user(
          username=f"{sajutoktok_prefix}counselor@email.com",
          password='123456a',
          first_name='상담사', # 사용자 실명
          last_name='테스트 상담사', # 사용자
          email='counselor@email.com', # 이메일
          user_data=json.dumps({
            'device_token': '', # 앱에서 푸시 메세지 발송을 위한 디바이스 토큰
            'push_allow': 'n', # 푸시 알림 허용 여부
            'ad_allow': 'n', # 광고 알림 허용 여부
            'type': 'counselor', # 계정 타입
            'account_status': 'active', # 계정 상태
            'counselor_categories': 'tarot,jum', # 상담사 사주 카테고리
            'counselor_services': 'tel,chat', # 상담사 제공 가능 서비스
            'online_auto_schedule_time': '00:00', # 상담사 자동 스케줄링 시간. 설정 시 해당 시간에 상담사 상태를 자동으로 online으로 변경.
            'online_auto_schedule_toggle': 'n', # 상담사 자동 스케줄링 사용 여부
            'offline_auto_schedule_time': '00:00', # 상담사 자동 스케줄링 시간. 설정 시 해당 시간에 상담사 상태를 자동으로 offline로 변경.
            'offline_auto_schedule_toggle': 'n', # 상담사 자동 스케줄링 사용 여부
            'online_status': '', # 상담가 온라인 상태
            'point': '0', # 보유 포인트(사용자: 사용 가능한 포인트, 상담사: 정산 가능한 포인트, 관리자: 정산된 누적 총 포인트)
            'tel': '01023456789', # 전화번호
            'address': '', # 주소
            'weight': '0', # 상담사 검색 가중치
            'profile_image_path': '/media/default.png', # 프로필 이미지 경로
            'introduce': '상담사 소갯말', # 상담사 소개
            'detail': '자유롭게 작성한 상담사 소갯말', # 상세 정보
            'like_users': '', # 상담사
            'supervisor_note': '', # 관리자 메모
          })
        )
        counselor.groups.add(sajutoktok_group)
      else:
        counselor = User.objects.get(username=f"{sajutoktok_prefix}counselor@email.com")

      # 더미 리뷰 메세지 작성
      if mo.REVIEW.objects.all().count() == 0:
        review = mo.REVIEW(
          user_id=user.email,
          counselor_id=counselor.email,
          payment_id='',
          content=f'상담사 {counselor.last_name}에 대한 리뷰입니다.',
          star='5',
        )
        review.save()

    except Exception as e:
      print('Error:', e)
      pass