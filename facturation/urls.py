from django.urls import path
from .views import ( 
    ClientView,
)

app_name = 'facturation'

urlpatterns = [
    path('clients/', ClientView.as_view(), name='vendor_list'),
]