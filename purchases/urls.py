from django.urls import path

from .views import ( VendorView, VendorNew, VendorUpdate,
    vendor_inactivate, PurchaseView, PurchaseNew, purchase, PurchaseDetailDelete
    )

app_name = 'purchases'

urlpatterns = [
    path('vendors/', VendorView.as_view(), name='vendor_list'),
    path('new-vendor/', VendorNew.as_view(), name='vendor_new'),
    path('edit-vendor/<int:pk>', VendorUpdate.as_view(), name='vendor_edit'),
    path('inactivate-vendor/<int:pk>', vendor_inactivate, name='vendor_inactivate'),
    path('purchases/', PurchaseView.as_view(), name='purchase_list'),
    path('edit-purchase/<int:pk>', purchase, name='purchase_edit'),
    path('new-purchase/', purchase, name='purchase_new'),
    path('purchase/delete/<int:pk>', PurchaseDetailDelete.as_view(), name='purchase_delete'),
]