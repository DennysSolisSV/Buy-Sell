from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class NotPrivileges(LoginRequiredMixin, PermissionRequiredMixin):
    login_url = reverse_lazy('bases:login')
    raise_exception = False
    redirect_field_name = 'redirect_to'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            self.login_url = 'bases:home_not_privileges'
            return HttpResponseRedirect(reverse_lazy(self.login_url))
        else:
            return super(NotPrivileges, self).handle_no_permission()

class Home(LoginRequiredMixin, generic.TemplateView):
    template_name = 'index.html'
    login_url = 'bases:login'

class HomeNotPrivileges(generic.TemplateView):
    template_name = 'bases/not_permit.html'
