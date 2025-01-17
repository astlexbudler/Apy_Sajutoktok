from django.db import models
import os
from datetime import datetime
import random
import string

'''
models.py: 데이터베이스 테이블을 정의합니다.

- CustomUser(AbstractUser): # 사용자 테이블
Django에서 기본으로 제공하는 AbstractUser를 상속받아 사용자 테이블을 정의합니다.
user_data: 사용자 정보를 JSON 형태로 저장합니다.
사용자 테이블에 대한 정의는 projects > applify > models.py에 있습니다.
앱에서 사용하기 위해서 별도의 설정은 필요하지 않습니다.

- UPLOAD(models.Model): # 업로드된 파일
파일 업로드 테이블을 정의합니다.
업로드된 시간을 파일명으로 사용합니다.

- ORM 설정과 관련하여..
일부 테이블은 자바스크립트를 통해서 데이터베이스에 엑세스할 수 있도록 API를 제공합니다.
이 경우, MetaData 클래스를 통해 API 권한을 설정할 수 있습니다.(읽기 및 쓰기 권한 설정. api 설정이 없으면 엑세스 불가)
models.fields의 default 설정에 에러가 발생할 수 있으므로, 필요한 경우 save 함수를 오버라이드하여 설정합니다.
되도록 CharField 또는 TextField를 사용하여 속성을 정의합니다.(JavaScript API에서 문자열 형태로 데이터를 전달하기 때문임)
'''
# models.py
# CustomUser: 사용자 테이블
# UPLOAD: 파일 업로드 테이블
# LOG: 서버 로그 테이블
# CERT_CODE: 이메일 인증 코드 테이블
# POST: 게시글 테이블
# COMMENT: 댓글 테이블
# REVIEW: 사용자 리뷰 테이블
# ITEM: 상담가 판매 상품 테이블
# PURCHASE: 상품 구매 테이블
# NOTIFICATION: 알림 테이블
# CHAT: 채팅 테이블
# SERVER_SETTING: 서버 설정 테이블

def upload_to(instance, filename):  # 파일 업로드 경로 및 파일명 설정
  _, ext = os.path.splitext(filename)
  new_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}{ext}"
  return os.path.join("sajutoktok/", new_filename)

def random_id(length): # 랜덤 아이디 생성(알파벳 + 숫자) *첫 글자는 반드시 알파벳
  return ''.join(random.choices(string.ascii_letters, k=1)) + ''.join(random.choices(string.ascii_letters + string.digits, k=length-1))



##########
# table
"""
CustomUser 테이블
  id = 사용자 식별용 아이디(이건 시스템에서 자동으로 생성)
  username = sajutoktok_{사용자 이메일} # 이걸로 로그인, 상담가의 경우 상담가 코드가 이메일을 대체함.
  password = 비밀번호(암호화된 비밀번호)
  first_name = 사용자 실명
  last_name = 사용자 닉네임
  email = 이메일 # 상담가의 경우 상담가 코드가 이메일을 대체함.
  is_active = 활성화 여부(비활성화시 로그인 불가)
  is_staff = 관리자 여부(admin 페이지 접근 가능 여부)
  is_superuser = 최고 관리자 여부(모든 권한 부여.)
  date_joined = 가입일시
  last_login = 마지막 로그인 일시(90일 이상 로그인 안한 계정은 sleeping 상태로 변경. 계정 복구로 다시 활성화 가능. 그 전까지는 로그인 불가.)
  groups = 사용자 그룹(sajutoktok 사용자 그룹)
  user_data = {
    device_token: '디바이스 토큰', # 앱에서 푸시 메세지 발송을 위한 디바이스 토큰
    push_allow: 'y, n', # 푸시 알림 허용 여부
    ad_allow: 'y, n', # 광고 알림 허용 여부
    type: 'user, counselor, supervisor', # 계정 타입
    account_status: 'active, deleted, sleeping', # 계정 상태
    counselor_categories: 'tarot, saju, jum', # 상담사 사주 카테고리
    counselor_services: 'tel, chat, meet, cafe', # 상담사 제공 가능 서비스
    online_auto_schedule_time: 'HH:MM', # 상담사 자동 스케줄링 시간. 설정 시 해당 시간에 상담사 상태를 자동으로 online으로 변경.
    online_auto_schedule_toggle: 'y, n', # 상담사 자동 스케줄링 사용 여부
    offline_auto_schedule_time: 'HH:MM', # 상담사 자동 스케줄링 시간. 설정 시 해당 시간에 상담사 상태를 자동으로 offline로 변경.
    offline_auto_schedule_toggle: 'y, n', # 상담사 자동 스케줄링 사용 여부
    online_status: 'online, offline, busy', # 상담가 온라인 상태
    point: 0, # 보유 포인트(사용자: 사용 가능한 포인트, 상담사: 정산 가능한 포인트)
    accumulated_point: 0, # 누적 포인트(사용자: 사용한 포인트, 상담사: 총 정산된 포인트)
    tel: '01012345678', # 전화번호
    address: '서울시 강남구 역삼동 123-456', # 주소
    weight: 0, # 상담사 검색 가중치
    profile_image_path: '프로필 이미지 경로', # 프로필 이미지 경로
    introduce: '자기소개', # 상담사 소개
    detail: '상세 정보', # 상세 정보
    like_users: '좋아요한 사용자 목록', # 상담사 좋아요
    supervisor_note: '관리자 메모', # 관리자 메모
  }
"""

class UPLOAD(models.Model): # file upload
  file = models.FileField(upload_to=upload_to)

class LOG(models.Model): # 서버 로그 테이블
  id = models.CharField(primary_key=True, max_length=16)
  log = models.TextField(help_text="시스템 로그 메세지")
  dt = models.CharField(max_length=20, help_text="YYYY-MM-DD HH:MM:SS")
  def save(self, *args, **kwargs):
    if not self.id or self.id == '0':
      self.id = random_id(16)
    if not self.dt or self.dt == '0':
      self.dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    super().save(*args, **kwargs)
  class MetaData:
    api_permission = {
      "id": "RW",
      "log": "RW",
      "dt": "RW",
    }

class CERT_CODE(models.Model): # 이메일 인증 코드 테이블
  code = models.CharField(primary_key=True, max_length=6)
  dt = models.CharField(max_length=20, help_text="YYYY-MM-DD HH:MM:SS")
  method_type = models.CharField(max_length=16, help_text="email, tel")
  method = models.CharField(max_length=16, help_text="user@email.com or 01012345678")
  def save(self, *args, **kwargs):
    if not self.code:
      self.code = ''.join(random.choices(string.digits, k=6))
    if not self.dt:
      self.dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    super().save(*args, **kwargs)

class POST(models.Model): # 게시글 테이블
  id = models.CharField(primary_key=True, max_length=16)
  author_id = models.CharField(max_length=64)
  qna_counselor_id = models.CharField(max_length=64, null=True, blank=True, help_text="질문 게시글의 경우 상담사 아이디")
  board = models.CharField(max_length=20, help_text="notice, event, qna, blog, faq")
  images = models.TextField(null=True, blank=True, help_text="게시글 이미지 경로들(,로 구분)")
  title = models.CharField(max_length=200)
  content = models.TextField()
  dt = models.CharField(max_length=20, help_text="YYYY-MM-DD HH:MM:SS")
  view_count = models.CharField(max_length=10, help_text="조회수")
  def save(self, *args, **kwargs):
    if not self.id or self.id == '0':
      self.id = random_id(16)
    if not self.dt or self.dt == '0':
      self.dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if not self.view_count or self.view_count == '0':
      self.view_count = '0'
    super().save(*args, **kwargs)
  class MetaData:
    api_permission = {
      "id": "RW",
      "author_id": "RW",
      "qna_counselor_id": "RW",
      "board": "RW",
      "images": "RW",
      "title": "RW",
      "content": "RW",
      "dt": "RW",
      "view_count": "RW",
    }

class COMMENT(models.Model): # 댓글 테이블
  id = models.CharField(primary_key=True, max_length=16)
  post_id = models.CharField(max_length=16)
  author_id = models.CharField(max_length=64)
  parent_comment_id = models.CharField(max_length=16, null=True, blank=True, help_text="부모 댓글 아이디")
  content = models.TextField()
  dt = models.CharField(max_length=20, help_text="YYYY-MM-DD HH:MM:SS")
  def save(self, *args, **kwargs):
    if not self.id or self.id == '0':
      self.id = random_id(16)
    if not self.dt or self.dt == '0':
      self.dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    super().save(*args, **kwargs)
  class MetaData:
    api_permission = {
      "id": "RW",
      "post_id": "RW",
      "author_id": "RW",
      "parent_comment_id": "RW",
      "content": "RW",
      "dt": "RW",
    }

class REVIEW(models.Model): # 사용자 리뷰 테이블
  id = models.CharField(primary_key=True, max_length=16)
  user_id = models.CharField(max_length=64)
  counselor_id = models.CharField(max_length=64)
  payment_id = models.CharField(max_length=16)
  content = models.TextField()
  star = models.CharField(max_length=1, help_text="1~5")
  dt = models.CharField(max_length=20, help_text="YYYY-MM-DD HH:MM:SS")
  def save(self, *args, **kwargs):
    if not self.id or self.id == '0':
      self.id = random_id(16)
    if not self.dt or self.dt == '0':
      self.dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    super().save(*args, **kwargs)
  class MetaData:
    api_permission = {
      "id": "RW",
      "user_id": "RW",
      "counselor_id": "RW",
      "payment_id": "RW",
      "content": "RW",
      "star": "RW",
      "dt": "RW",
    }

class ITEM(models.Model): # 상담가 핀매 상품 테이블
  id = models.CharField(primary_key=True, max_length=16)
  counselor_id = models.CharField(max_length=64, help_text="상담사 아이디")
  name = models.CharField(max_length=64, help_text="상품명")
  item_status = models.CharField(max_length=20, help_text="display, hide, soldout")
  item_service = models.CharField(max_length=20, help_text="taro, saju, jum")
  item_category = models.CharField(max_length=20, help_text="tel, chat, meet, cafe")
  image = models.CharField(max_length=200, help_text="상품 이미지 경로")
  description = models.TextField(help_text="상품 설명")
  price = models.CharField(max_length=60)
  def save(self, *args, **kwargs):
    if not self.id or self.id == '0':
      self.id = random_id(16)
    if not self.price or self.price == '0':
      self.price = '0'
    super().save(*args, **kwargs)
  class MetaData:
    api_permission = {
      "id": "RW",
      "counselor_id": "RW",
      "name": "RW",
      "item_status": "RW",
      "item_service": "RW",
      "item_category": "RW",
      "image": "RW",
      "description": "RW",
      "price": "RW",
    }

class PURCHASE(models.Model): # 상품 구매 테이블
  id = models.CharField(primary_key=True, max_length=16)
  user_id = models.CharField(max_length=64)
  counselor_id = models.CharField(max_length=64)
  item_id = models.CharField(max_length=16)
  price = models.CharField(max_length=60)
  duration_seconds = models.CharField(max_length=20, help_text="상품 이용 시간(초)")
  pgcode = models.CharField(max_length=20, help_text="item, point, adjust, pgcode")
  cid = models.CharField(max_length=200, help_text="pg사 거래번호 또는 상담사 아이디")
  tid = models.CharField(max_length=200, null=True, blank=True, help_text="pg사 거래번호")
  status = models.CharField(max_length=20, help_text="pending, completed, reviewed, canceled, refunded")
  log = models.TextField(null=True, blank=True, help_text="거래 메세지")
  token = models.CharField(max_length=100, null=True, blank=True, help_text="pg사 거래 토큰")
  dt = models.CharField(null=True, blank=True, max_length=16, help_text="YYYY-MM-DD HH:MM:SS")
  def save(self, *args, **kwargs):
    if not self.id or self.id == '0':
      self.id = random_id(16)
    if not self.dt or self.dt == '0':
      self.dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    super().save(*args, **kwargs)
  class MetaData:
    api_permission = {
      "id": "RW",
      "user_id": "RW",
      "counselor_id": "RW",
      "item_id": "RW",
      "price": "RW",
      "duration_seconds": "RW",
      "pgcode": "RW",
      "cid": "RW",
      "tid": "RW",
      "status": "RW",
      "log": "RW",
      "token": "RW",
      "dt": "RW",
    }

class NOTIFICATION(models.Model): # 알림 테이블
  id = models.CharField(primary_key=True, max_length=16)
  account_id = models.CharField(max_length=64)
  title = models.CharField(max_length=200)
  content = models.TextField()
  link = models.CharField(max_length=200, null=True, blank=True)
  dt = models.CharField(max_length=20, help_text="YYYY-MM-DD HH:MM:SS")
  def save(self, *args, **kwargs):
    if not self.id or self.id == '0':
      self.id = random_id(16)
    if not self.dt or self.dt == '0':
      self.dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    super().save(*args, **kwargs)
  class MetaData:
    api_permission = {
      "id": "RW",
      "account_id": "RW",
      "title": "RW",
      "content": "RW",
      "link": "RW",
      "dt": "RW",
    }

class CHAT(models.Model): # 채팅 테이블
  id = models.CharField(primary_key=True, max_length=16)
  from_id = models.CharField(max_length=64)
  to_id = models.CharField(max_length=64)
  content = models.TextField()
  dt = models.CharField(max_length=20, help_text="YYYY-MM-DD HH:MM:SS")
  read = models.CharField(max_length=1, help_text="y, n")
  chat_type = models.CharField(max_length=20, help_text="image, item, purchase")
  def save(self, *args, **kwargs):
    if not self.id or self.id == '0':
      self.id = random_id(16)
    if not self.dt or self.dt == '0':
      self.dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    if not self.read or self.read == '0':
      self.read = 'n'
    super().save(*args, **kwargs)
  class MetaData:
    api_permission = {
      "id": "RW",
      "from_id": "RW",
      "to_id": "RW",
      "content": "RW",
      "dt": "RW",
      "read": "RW",
      "chat_type": "RW",
    }

class SERVER_SETTING(models.Model): # 서버 설정 테이블
  id = models.CharField(primary_key=True, max_length=16)
  key = models.CharField(max_length=64)
  value = models.TextField()
  class MetaData:
    api_permission = {
      "id": "RW",
      "key": "RW",
      "value": "RW",
    }
  def save(self, *args, **kwargs):
    if not self.id or self.id == '0':
      self.id = random_id(16)
    super().save(*args, **kwargs)

