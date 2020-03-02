from django.contrib import admin

from accounts.models import User, UserInfo

admin.site.register([User, UserInfo])