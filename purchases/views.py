from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from bases.views import NotPrivileges

import datetime
import json 
from .forms import VendorForm, PurchaseForm
from .models import Vendor, PurchaseDetail, Purchase
from inventory.models import Product

class VendorView(NotPrivileges, ListView):
    permission_required = 'purchases.view_vendor'
    model =  Vendor
    template_name = 'purchases/vendor_list.html'
    context_object_name =  'obj'


class VendorNew(NotPrivileges, CreateView):
    permission_required = 'purchases.add_vendor'
    model = Vendor
    template_name = 'purchases/vendor_form.html'
    form_class = VendorForm
    success_url = reverse_lazy('purchases:vendor_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class VendorUpdate(NotPrivileges, UpdateView):
    permission_required = 'purchases.change_vendor'
    model = Vendor
    template_name = 'purchases/vendor_form.html'
    form_class = VendorForm
    success_url = reverse_lazy('purchases:vendor_list')
    context_object_name = "obj"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

@login_required(login_url='/login/')
@permission_required('purchases.change_vendor', login_url='bases:home_not_privileges')
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

class PurchaseView(NotPrivileges, ListView):
    permission_required = 'purchases.view_purchase'
    model =  Purchase
    template_name = 'purchases/purchases_list.html'
    context_object_name =  'obj'

class PurchaseNew(NotPrivileges, CreateView):
    permission_required = 'purchases.add_purchase'
    model = Purchase
    template_name = 'purchases/purchase.html'
    form_class = PurchaseForm
    success_url = reverse_lazy('purchases:purchase_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

@login_required(login_url='/login/')
@permission_required('purchase.view_purchase', login_url='bases:home_not_privileges')
def purchase(request, pk=None):
    template_name= 'purchases/purchase.html'
    products = Product.objects.filter(status=True)
    form_purchase = {}
    context = {}

    if request.method == 'GET':
        purchase = Purchase.objects.filter(pk=pk).first()

        if purchase:
            detail = PurchaseDetail.objects.filter(purchase=purchase)
            date_purchase = datetime.date.isoformat(purchase.date_purchase)
            date_invoice = datetime.date.isoformat(purchase.date_invoice)

            # initializing form if exist
            data = {
                'date_purchase': date_purchase,
                'vendor': purchase.vendor,
                'observations': purchase.observations,
                'invoice_number': purchase.invoice_number,
                'date_invoice': purchase.date_invoice,
                'sub_total': purchase.sub_total,
                'discount': purchase.discount,
                'total': purchase.total
            }

            form_purchase = PurchaseForm(data)
        else:
            detail = None
            form_purchase = PurchaseForm()


        context={
            'products': products, 
            'header': purchase, 
            'detail': detail,
            'form_purchase': form_purchase
        }

        return render(request, template_name, context)

