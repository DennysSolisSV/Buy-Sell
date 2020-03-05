from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
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
    purchase_pk = pk
    new_purchase = False

    if request.method == 'GET':
        purchase = Purchase.objects.filter(pk=purchase_pk).first()

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


        context = {
            'products': products, 
            'header': purchase, 
            'detail': detail,
            'form_purchase': form_purchase
        }    

    if request.method == 'POST':
        date_purchase = request.POST.get("date_purchase")
        observations = request.POST.get("observations")
        invoice_number = request.POST.get("invoice_number")
        date_invoice = request.POST.get("date_invoice")
        vendor = request.POST.get("vendor")
        sub_total = 0
        discount = 0
        total = 0

        # For a new purchase
        if not purchase_pk:
            new_purchase = True
            vendor=Vendor.objects.get(pk=vendor)

            purchase = Purchase(
                date_purchase = date_purchase,
                observations = observations,
                invoice_number = invoice_number,
                date_invoice = date_invoice,
                vendor = vendor,
                created_by = request.user 
            )
            if purchase:
                purchase.save()
                purchase_pk = purchase.pk


        #  Updating purchase        
        else:
            purchase = Purchase.objects.filter(pk=purchase_pk).first()
            if purchase:
                purchase.date_purchase = date_purchase
                purchase.observations = observations
                purchase.invoice_number = invoice_number
                purchase.date_invoice = date_invoice
                purchase.updated_by = request.user
                purchase.save()

            # return redirect("purchases:purchase_list")

        #  Getting values from detail 

        product_id = request.POST.get("id_id_product")
        quantity = request.POST.get("id_quantity_detail")
        price = request.POST.get("id_price_detail")
        sub_total_detail = request.POST.get("id_sub_total_detail")
        discount_detail  = request.POST.get("id_discount_detail")
        total_detail  = request.POST.get("id_total_detail")

        if product_id:
            product = Product.objects.get(pk=product_id)

            detail = PurchaseDetail(
                purchase=purchase,
                product=product,
                quantity=quantity,
                price=price,
                discount=discount_detail,
                cost=0,
                created_by=request.user
            )

            if detail:
                detail.save()

                sub_total = PurchaseDetail.objects.filter(purchase=purchase_pk).aggregate(Sum('sub_total'))
                discount = PurchaseDetail.objects.filter(purchase=purchase_pk).aggregate(Sum('discount'))
                purchase.sub_total = sub_total["sub_total__sum"]
                purchase.discount = discount["discount__sum"]
                purchase.save()

        if new_purchase:
            return redirect("purchases:purchase_edit", pk = purchase_pk)

        return redirect("purchases:purchase_list")


    return render(request, template_name, context)


class PurchaseDetailDelete(NotPrivileges, DeleteView): 
    permission_required = "purchases.delete_purchasedetail"
    model = PurchaseDetail
    template_name = "purchases/purchase_detail_delete.html"
    context_object_name = "obj"

    def get_success_url(self):
        purchase_pk = self.kwargs['pk']
        return redirect("purchases:purchase_edit", pk = purchase_pk)