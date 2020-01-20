from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import (
    Category, SubCategory, Brand, UnitOfMeasurement,
    Product,
)

from .forms import (
    CategoryForm, SubCategoryForm, BrandForm, 
    UnitOfMeasurementForm, ProductForm,
)

# CATEGORY VIEWS (CRUD)

class CategoryView(LoginRequiredMixin, ListView):
    model =  Category
    template_name = 'inventory/category_list.html'
    context_object_name =  'obj'
    login_url = reverse_lazy('bases:login')


class CategoryNew(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'inventory/category_form.html'
    form_class = CategoryForm
    success_url = reverse_lazy('inventory:category_list')
    login_url = reverse_lazy('bases:login')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class CategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = 'inventory/category_form.html'
    form_class = CategoryForm
    success_url = reverse_lazy('inventory:category_list')
    login_url = reverse_lazy('bases:login')
    context_object_name = "obj"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'inventory/catalog_del.html'
    context_object_name = 'obj'
    success_url = reverse_lazy('inventory:category_list')


# SUBCATEGORY VIEWS (CRUD)

class SubcategoryView(LoginRequiredMixin, ListView):
    model =  SubCategory
    template_name = 'inventory/subcategory_list.html'
    context_object_name =  'obj'
    login_url = reverse_lazy('bases:login')


class SubCategoryNew(LoginRequiredMixin, CreateView):
    model = SubCategory
    template_name = 'inventory/subcategory_form.html'
    form_class = SubCategoryForm
    success_url = reverse_lazy('inventory:subcategory_list')
    login_url = reverse_lazy('bases:login')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class SubCategoryUpdate(LoginRequiredMixin, UpdateView):
    model = SubCategory
    template_name = 'inventory/subcategory_form.html'
    form_class = SubCategoryForm
    success_url = reverse_lazy('inventory:subcategory_list')
    login_url = reverse_lazy('bases:login')
    context_object_name = "obj"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class SubCategoryDelete(LoginRequiredMixin, DeleteView):
    model = SubCategory
    template_name = 'inventory/catalog_del.html'
    context_object_name = 'obj'
    success_url = reverse_lazy('inventory:subcategory_list')


# BRAND VIEWS (CRUD) 

class BrandsView(LoginRequiredMixin, ListView):
    model =  Brand
    template_name = 'inventory/brand_list.html'
    context_object_name =  'obj'
    login_url = reverse_lazy('bases:login')


class BrandNew(LoginRequiredMixin, CreateView):
    model = Brand
    template_name = 'inventory/brand_form.html'
    form_class = BrandForm
    success_url = reverse_lazy('inventory:brand_list')
    login_url = reverse_lazy('bases:login')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class BrandUpdate(LoginRequiredMixin, UpdateView):
    model = Brand
    template_name = 'inventory/brand_form.html'
    form_class = BrandForm
    success_url = reverse_lazy('inventory:brand_list')
    login_url = reverse_lazy('bases:login')
    context_object_name = "obj"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


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
        else:
            brand.status = True
        brand.save()

        return redirect("inventory:brand_list")

    return render(request, template_name, context)


# UNIT OF MEASUREMENT VIEWS

class UnitOfMeasurementView(LoginRequiredMixin, ListView):
    model =  UnitOfMeasurement
    template_name = 'inventory/unit_of_measurement_list.html'
    context_object_name =  'obj'
    login_url = reverse_lazy('bases:login')


class UnitOfMeasurementNew(LoginRequiredMixin, CreateView):
    model = UnitOfMeasurement
    template_name = 'inventory/unit_of_measurement_form.html'
    form_class = UnitOfMeasurementForm
    success_url = reverse_lazy('inventory:unit_of_measurement_list')
    login_url = reverse_lazy('bases:login')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class UnitOfMeasurementUpdate(LoginRequiredMixin, UpdateView):
    model = UnitOfMeasurement
    template_name = 'inventory/unit_of_measurement_form.html'
    form_class = UnitOfMeasurementForm
    success_url = reverse_lazy('inventory:unit_of_measurement_list')
    login_url = reverse_lazy('bases:login')
    context_object_name = "obj"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


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

class ProductsView(LoginRequiredMixin, ListView):
    model =  Product
    template_name = 'inventory/product_list.html'
    context_object_name =  'obj'
    login_url = reverse_lazy('bases:login')


class ProductNew(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'inventory/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('inventory:product_list')
    login_url = reverse_lazy('bases:login')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'inventory/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('inventory:product_list')
    login_url = reverse_lazy('bases:login')
    context_object_name = "obj"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


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