from django.core.exceptions import PermissionDenied
from django.views.generic.base import View
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class BaseView(LoginRequiredMixin, PermissionRequiredMixin, View):

    context = {}
    template_name = ''
    permission_required = ()

    def dispatch(self, request, *args, **kwargs):
        self.context = {}
        return super(BaseView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        has_perm = self.has_object_permission(request, args, kwargs)
        self.handle_permission_denied(has_perm)

    def post(self,request, *args, **kwargs):
        has_perm = self.has_object_permission(request, args, kwargs)
        self.handle_permission_denied(has_perm)

    def has_object_permission(self, request, *args, **kwargs):
        user = request.user

        if user:
            return True

        return False

    @staticmethod
    def handle_permission_denied(has_perm):
        msg = 'You don\'t have permission to view this object'

        if not has_perm:
            raise PermissionDenied(msg)