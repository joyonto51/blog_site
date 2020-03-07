from django.shortcuts import render

from accounts.models import User
from blog_site.views import BaseView


class MessengerView(BaseView):
    template_name = 'messenger2.html'

    def get(self, request, *args, **kwargs):

        context = {
            'users': User.objects.all().exclude(id=request.user.id)
        }
        return render(request, self.template_name, context)