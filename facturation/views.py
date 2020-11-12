from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from datetime import datetime
from bases.views import NotPrivileges

from .models import Client, InvoiceHeader
from .forms import ClientForm

from django.http import HttpResponse


class ClientView(NotPrivileges, ListView):
    permission_required = 'facturation.view_client'
    model = Client
    template_name = 'facturation/client_list.html'
    context_object_name = 'obj'


class CreateViewBase(SuccessMessageMixin, NotPrivileges, CreateView):
    context_object_name = 'obj'
    success_message = 'Successfully added'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class UpdateViewBase(SuccessMessageMixin, NotPrivileges, UpdateView):
    context_object_name = 'obj'
    success_message = 'Successfully updated'
    
    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ClientNew(CreateViewBase):
    model = Client
    template_name = 'facturation/client_form.html'
    form_class = ClientForm
    success_url = reverse_lazy('facturation:client_list')
    permission_required = 'facturation.add_client'


class ClientUpdate(UpdateViewBase):
    model = Client
    template_name = 'facturation/client_form.html'
    form_class = ClientForm
    success_url = reverse_lazy('facturation:client_list')
    permission_required = 'facturation.change_client'

@login_required(login_url='/login/')
@permission_required('facturation.change_client', login_url='bases:home_not_privileges')
def change_status(request, pk):
    client = Client.objects.get(pk = pk)
    
    if request.method == 'POST':
        if client:
            client.status = not client.status
            client.save()

            return HttpResponse('OK')
        return HttpResponse('FAIL')
    return HttpResponse('FAIL')
    

class InvoicesView(NotPrivileges, ListView):
    permission_required = 'facturation.view_invoiceheader'
    model = InvoiceHeader
    template_name = 'facturation/invoices_list.html'
    context_object_name = 'obj'

@login_required(login_url='/login/')
@permission_required('facturation.change_invoiceheader', login_url='bases:home_not_privileges')
def invoices(request, id=None):
    template_name = 'facturation/invoices.html'

    context = {
        'date':datetime.today()
    }
    return render(request, template_name, context)