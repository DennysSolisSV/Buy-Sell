from django.urls import path
from .views import ( 
    ClientView, ClientNew, ClientUpdate, change_status,
    InvoicesView, invoices
)

app_name = 'facturation'

urlpatterns = [
    path('clients/', ClientView.as_view(), name='client_list'),
    path('clients/new', ClientNew.as_view(), name='client_new'),
    path('clients/<int:pk>', ClientUpdate.as_view(), name='client_edit'),
    path('clients/ajax/change/status/<int:pk>', change_status, name='ajax_change_status'),
    path('invoices/list/', InvoicesView.as_view(), name='invoices_list'),
    path('invoice/new/', invoices, name='new_invoice'),
]