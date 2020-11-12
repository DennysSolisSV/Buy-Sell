from django.contrib import admin
from .models import Client, InvoiceHeader, InvoiceDetail

admin.site.register(Client)
admin.site.register(InvoiceHeader)
admin.site.register(InvoiceDetail)
