from django.shortcuts import render
from django.views.generic import ListView
from bases.views import NotPrivileges

from .models import Client


class ClientView(NotPrivileges, ListView):
    permission_required = 'facturation.view_client'
    model = Client
    template_name = 'facturation/client_list.html'
    context_object_name = 'obj'
