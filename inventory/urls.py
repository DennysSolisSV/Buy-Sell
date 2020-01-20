from django.urls import path

from .views import (
    CategoryView, CategoryNew, 
    CategoryUpdate, CategoryDelete,
    SubcategoryView,SubCategoryNew,
    SubCategoryUpdate, SubCategoryDelete,
    BrandsView, BrandNew, BrandUpdate, 
    brand_activate_deactivate,UnitOfMeasurementView, 
    UnitOfMeasurementNew, UnitOfMeasurementUpdate, 
    unit_of_measurement_activate_deactivate,
    ProductsView, ProductNew, ProductUpdate,
    product_activate_deactivate,
    )

app_name = 'inventory'

urlpatterns = [
    path('categories/', CategoryView.as_view(), name='category_list'),
    path('new-category/', CategoryNew.as_view(), name='category_new'),
    path('edit-category/<int:pk>', CategoryUpdate.as_view(), name='category_edit'),
    path('delete-category/<int:pk>', CategoryDelete.as_view(), name='category_del'),

    path('subcategories/', SubcategoryView.as_view(), name='subcategory_list'),
    path('new-subcategory/', SubCategoryNew.as_view(), name='subcategory_new'),
    path('edit-subcategory/<int:pk>', SubCategoryUpdate.as_view(), name='subcategory_edit'),
    path('delete-subcategory/<int:pk>', SubCategoryDelete.as_view(), name='subcategory_del'),

    path('brands/', BrandsView.as_view(), name='brand_list'),
    path('new-brand/', BrandNew.as_view(), name='brand_new'),
    path('edit-brand/<int:pk>', BrandUpdate.as_view(), name='brand_edit'),
    path('act-inactive-brand/<int:id>', brand_activate_deactivate, name='brand_act-inac'),

    path('units/', UnitOfMeasurementView.as_view(), name='unit_of_measurement_list'),
    path('new-unit/', UnitOfMeasurementNew.as_view(), name='unit_of_measurement_new'),
    path('edit-unit/<int:pk>', UnitOfMeasurementUpdate.as_view(), name='unit_of_measurement_edit'),
    path('act-inactive-unit/<int:id>', unit_of_measurement_activate_deactivate, name='unit_of_measurement_act-inac'),

    path('products/', ProductsView.as_view(), name='product_list'),
    path('new-product/', ProductNew.as_view(), name='product_new'),
    path('edit-product/<int:pk>', ProductUpdate.as_view(), name='product_edit'),
    path('act-inactive-product/<int:id>', product_activate_deactivate, name='product_act-inac'),
]