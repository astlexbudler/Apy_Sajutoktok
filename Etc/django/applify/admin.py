from django.contrib import admin
from . import models as mo

class CustomUserAdmin(admin.ModelAdmin):
  list_display = ['id', 'username', 'email', 'date_joined']
  search_fields = ['id', 'username', 'email']
  list_filter = ['date_joined']
admin.site.register(mo.CustomUser, CustomUserAdmin)