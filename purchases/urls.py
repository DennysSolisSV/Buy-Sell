from django.urls import path

from .views import ( VendorView, VendorNew, VendorUpdate,
    vendor_inactivate,
    )

app_name = 'purchases'

urlpatterns = [
    path('vendors/', VendorView.as_view(), name='vendor_list'),
    path('new-vendor/', VendorNew.as_view(), name='vendor_new'),
    path('edit-vendor/<int:pk>', VendorUpdate.as_view(), name='vendor_edit'),
    path('inactivate-vendor/<int:pk>', vendor_inactivate, name='vendor_inactivate'),
]