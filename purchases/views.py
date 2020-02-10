from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView


import json 
from .forms import VendorForm
from .models import Vendor

class VendorView(LoginRequiredMixin, ListView):
    model =  Vendor
    template_name = 'purchases/vendor_list.html'
    context_object_name =  'obj'
    login_url = reverse_lazy('bases:login')


class VendorNew(LoginRequiredMixin, CreateView):
    model = Vendor
    template_name = 'purchases/vendor_form.html'
    form_class = VendorForm
    success_url = reverse_lazy('purchases:vendor_list')
    login_url = reverse_lazy('bases:login')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class VendorUpdate(LoginRequiredMixin, UpdateView):
    model = Vendor
    template_name = 'purchases/vendor_form.html'
    form_class = VendorForm
    success_url = reverse_lazy('purchases:vendor_list')
    login_url = reverse_lazy('bases:login')
    context_object_name = "obj"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

def vendor_inactivate(request, pk):
    template_name = 'purchases/inactivate_vendor.html'
    obj = Vendor.objects.filter(pk=pk).first()

    if not obj:
        return HttpResponse('Vendor not found ('+ str(pk) +')' )

    if request.method == 'GET':
        context = {'obj': obj}

    if request.method == 'POST':
        if obj.status == True:
            obj.status = False
            msg = 'Vendor Inactivated'
        else:
            obj.status = True
            msg = 'Vendor Activate'

        obj.save()
        context = {'obj': 'OK'}
        return  HttpResponse(msg)

    return render(request, template_name, context)
