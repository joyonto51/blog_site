from django.shortcuts import render
from django.views.generic.base import View

from blog.models import Blog


class BlogListView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'blogs': Blog.objects.all(),
        }

        return render(request, 'blog.html', context)