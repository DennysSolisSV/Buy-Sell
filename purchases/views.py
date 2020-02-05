from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

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