from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from django.contrib import messages

from django.contrib.auth.decorators import login_required, permission_required

from .models import (
    Category, SubCategory, Brand, UnitOfMeasurement,
    Product,
)

from .forms import (
    CategoryForm, SubCategoryForm, BrandForm, 
    UnitOfMeasurementForm, ProductForm,
)

from bases.views import NotPrivileges

# CATEGORY VIEWS (CRUD)

class CategoryView(NotPrivileges, ListView):
    permission_required = 'inventory.view_category'
    model =  Category
    template_name = 'inventory/category_list.html'
    context_object_name =  'obj'
    


class CategoryNew(SuccessMessageMixin, NotPrivileges, CreateView):
    permission_required = 'inventory.add_category'
    model = Category
    template_name = 'inventory/category_form.html'
    form_class = CategoryForm
    success_url = reverse_lazy('inventory:category_list')
    success_message =  "Category created"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class CategoryUpdate(SuccessMessageMixin, NotPrivileges, UpdateView):
    permission_required = 'inventory.change_category'
    model = Category
    template_name = 'inventory/category_form.html'
    form_class = CategoryForm
    success_url = reverse_lazy('inventory:category_list')
    context_object_name = "obj"
    success_message = "Edited"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class CategoryDelete(NotPrivileges, DeleteView):
    permission_required = 'inventory.delete_category'
    model = Category
    template_name = 'inventory/catalog_del.html'
    context_object_name = 'obj'
    success_url = reverse_lazy('inventory:category_list')


# SUBCATEGORY VIEWS (CRUD)

class SubcategoryView(NotPrivileges, ListView):
    permission_required = 'inventory.view_subcategory'
    model =  SubCategory
    template_name = 'inventory/subcategory_list.html'
    context_object_name =  'obj'


class SubCategoryNew(NotPrivileges, CreateView):
    permission_required = 'inventory.add_subcategory'
    model = SubCategory
    template_name = 'inventory/subcategory_form.html'
    form_class = SubCategoryForm
    success_url = reverse_lazy('inventory:subcategory_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class SubCategoryUpdate(NotPrivileges, UpdateView):
    permission_required = 'inventory.change_subcategory'
    model = SubCategory
    template_name = 'inventory/subcategory_form.html'
    form_class = SubCategoryForm
    success_url = reverse_lazy('inventory:subcategory_list')
    context_object_name = "obj"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class SubCategoryDelete(DeleteView):
    permission_required = 'inventory.delete_subcategory'
    model = SubCategory
    template_name = 'inventory/catalog_del.html'
    context_object_name = 'obj'
    success_url = reverse_lazy('inventory:subcategory_list')


# BRAND VIEWS (CRUD) 

class BrandsView(NotPrivileges, ListView):
    permission_required = 'inventory.view_brand'
    model =  Brand
    template_name = 'inventory/brand_list.html'
    context_object_name =  'obj'

class BrandNew(NotPrivileges, CreateView):
    permission_required = 'inventory.add_brand'
    model = Brand
    template_name = 'inventory/brand_form.html'
    form_class = BrandForm
    success_url = reverse_lazy('inventory:brand_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class BrandUpdate(NotPrivileges, UpdateView):
    permission_required = 'inventory.change_brand'
    model = Brand
    template_name = 'inventory/brand_form.html'
    form_class = BrandForm
    success_url = reverse_lazy('inventory:brand_list')
    context_object_name = "obj"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

@login_required(login_url='/login/')
@permission_required('inventory.change_brand', login_url='bases:home_not_privileges')
def brand_activate_deactivate(request, id):
    brand = Brand.objects.get(pk=id)
    context = {}
    template_name = "inventory/catalog_del.html"

    if not brand:
        return redirect("inventory:brand_list")

    if request.method == "GET":
        context = { 'obj': brand}
    else:
        if brand.status == True:
            brand.status = False
            messages.add_message(request, messages.WARNING, "Brand Inactivated!" )
        else:
            brand.status = True
            messages.add_message(request, messages.SUCCESS, "Brand Activated!" )
        brand.save()
        
        return redirect("inventory:brand_list")

    return render(request, template_name, context)


# UNIT OF MEASUREMENT VIEWS

class UnitOfMeasurementView(NotPrivileges, ListView):
    permission_required = 'inventory.view_unitofmeasurement'
    model =  UnitOfMeasurement
    template_name = 'inventory/unit_of_measurement_list.html'
    context_object_name =  'obj'


class UnitOfMeasurementNew(NotPrivileges, CreateView):
    permission_required = 'inventory.add_unitofmeasurement'
    model = UnitOfMeasurement
    template_name = 'inventory/unit_of_measurement_form.html'
    form_class = UnitOfMeasurementForm
    success_url = reverse_lazy('inventory:unit_of_measurement_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class UnitOfMeasurementUpdate(NotPrivileges, UpdateView):
    permission_required = 'inventory.change_unitofmeasurement'
    model = UnitOfMeasurement
    template_name = 'inventory/unit_of_measurement_form.html'
    form_class = UnitOfMeasurementForm
    success_url = reverse_lazy('inventory:unit_of_measurement_list')
    context_object_name = "obj"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

@login_required(login_url='/login/')
@permission_required('inventory.change_unitofmeasurement', login_url='bases:home_not_privileges')
def unit_of_measurement_activate_deactivate(request, id):
    unit_of_measurement = UnitOfMeasurement.objects.get(pk=id)
    context = {}
    template_name = "inventory/catalog_del.html"

    if not unit_of_measurement:
        return redirect("inventory:unit_of_measurement_list")

    if request.method == "GET":
        context = { 'obj': unit_of_measurement}
    else:
        if unit_of_measurement.status == True:
            unit_of_measurement.status = False
        else:
            unit_of_measurement.status = True
        unit_of_measurement.save()
        
        return redirect("inventory:unit_of_measurement_list")

    return render(request, template_name, context)


# PRODUCT VIEWS 

class ProductsView(NotPrivileges, ListView):
    permission_required = 'inventory.view_product'
    model =  Product
    template_name = 'inventory/product_list.html'
    context_object_name =  'obj'


class ProductNew(NotPrivileges, CreateView):
    permission_required = 'inventory.add_product'
    model = Product
    template_name = 'inventory/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('inventory:product_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ProductUpdate(NotPrivileges, UpdateView):
    permission_required = 'inventory.change_product'
    model = Product
    template_name = 'inventory/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('inventory:product_list')
    context_object_name = "obj"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

@login_required(login_url='/login/')
@permission_required('inventory.change_product', login_url='bases:home_not_privileges')
def product_activate_deactivate(request, id):
    product = Product.objects.get(pk=id)
    context = {}
    template_name = "inventory/catalog_del.html"

    if not product:
        return redirect("inventory:product_list")

    if request.method == "GET":
        context = { 'obj': product}
    else:
        if product.status == True:
            product.status = False
        else:
            product.status = True
        product.save()

        return redirect("inventory:product_list")

    return render(request, template_name, context)