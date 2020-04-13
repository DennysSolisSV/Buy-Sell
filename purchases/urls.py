from django.urls import path
from .views import ( VendorView, VendorNew, VendorUpdate,\
    vendor_inactivate, PurchaseView, purchase, PurchaseDetailDelete,
)

from .reports import report_purchases, report_purchase
app_name = 'purchases'

urlpatterns = [
    path('vendors/', VendorView.as_view(), name='vendor_list'),
    path('new-vendor/', VendorNew.as_view(), name='vendor_new'),
    path('edit-vendor/<int:pk>', VendorUpdate.as_view(), name='vendor_edit'),
    path('inactivate-vendor/<int:pk>', vendor_inactivate, name='vendor_inactivate'),
    path('purchases/', PurchaseView.as_view(), name='purchase_list'),
    path('edit-purchase/<int:pk>', purchase, name='purchase_edit'),
    path('new-purchase/', purchase, name='purchase_new'),
    path('<int:purchase_pk>/delete/<int:pk>', PurchaseDetailDelete.as_view(), name='purchase_detail_delete'),
    path('report/purchases/list', report_purchases, name='report_purchases'),
    path('report/purchase/print/<int:purchase_pk>', report_purchase, name="report_purchase"),
]