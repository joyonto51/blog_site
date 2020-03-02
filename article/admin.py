from django.contrib import admin

from article.models import Category, Article, Comment

admin.site.register([Category, Article, Comment])