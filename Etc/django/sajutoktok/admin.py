from django.contrib import admin
from .models import *

# admin.py는 왠만하면 직접 작성하지 말고, 생성형 모델을 사용해서 자동으로 생성하자.

class UploadAdmin(admin.ModelAdmin):
  list_display = ['file']
  search_fields = ['file']
  list_filter = ['file']

class LogAdmin(admin.ModelAdmin):
  list_display = ['id', 'log', 'dt']
  search_fields = ['id', 'log']
  list_filter = ['dt']

class CertCodeAdmin(admin.ModelAdmin):
  list_display = ['code', 'dt', 'method_type', 'method']
  search_fields = ['code', 'method']
  list_filter = ['dt', 'method_type']

class PostAdmin(admin.ModelAdmin):
  list_display = ['id', 'author_id', 'title', 'dt', 'view_count']
  search_fields = ['id', 'author_id', 'title']
  list_filter = ['dt', 'board']

class CommentAdmin(admin.ModelAdmin):
  list_display = ['id', 'post_id', 'author_id', 'content', 'dt']
  search_fields = ['id', 'post_id', 'author_id']
  list_filter = ['dt']

class ReviewAdmin(admin.ModelAdmin):
  list_display = ['id', 'user_id', 'counselor_id', 'content', 'star', 'dt']
  search_fields = ['id', 'user_id', 'counselor_id']
  list_filter = ['dt', 'star']

class ItemAdmin(admin.ModelAdmin):
  list_display = ['id', 'counselor_id', 'name', 'item_status', 'item_service', 'item_category', 'price']
  search_fields = ['id', 'counselor_id', 'name']
  list_filter = ['item_status', 'item_service', 'item_category']

class PurchaseAdmin(admin.ModelAdmin):
  list_display = ['id', 'user_id', 'counselor_id', 'item_id', 'price', 'status', 'dt']
  search_fields = ['id', 'user_id', 'counselor_id', 'item_id']
  list_filter = ['status', 'dt']

class NotificationAdmin(admin.ModelAdmin):
  list_display = ['id', 'account_id', 'title', 'dt']
  search_fields = ['id', 'account_id', 'title']
  list_filter = ['dt']

class ChatAdmin(admin.ModelAdmin):
  list_display = ['id', 'from_id', 'to_id', 'content', 'dt', 'read', 'chat_type']
  search_fields = ['id', 'from_id', 'to_id', 'content']
  list_filter = ['dt', 'read', 'chat_type']

class ServerSettingAdmin(admin.ModelAdmin):
  list_display = ['id', 'key', 'value']
  search_fields = ['id', 'key']
  list_filter = ['key']

admin.site.register(UPLOAD, UploadAdmin)
admin.site.register(LOG, LogAdmin)
admin.site.register(CERT_CODE, CertCodeAdmin)
admin.site.register(POST, PostAdmin)
admin.site.register(COMMENT, CommentAdmin)
admin.site.register(REVIEW, ReviewAdmin)
admin.site.register(ITEM, ItemAdmin)
admin.site.register(PURCHASE, PurchaseAdmin)
admin.site.register(NOTIFICATION, NotificationAdmin)
admin.site.register(CHAT, ChatAdmin)
admin.site.register(SERVER_SETTING, ServerSettingAdmin)
