from django.db import models
from inventory.models import ClassModel, ClassModel2
from inventory.models import Product
from django.urls import reverse

class Client(ClassModel):
    TYPES = (
        ('natural', 'Natural'),
        ('juridical', 'Juridical'),

    )
    name = models.CharField(
        max_length=100
    )
    lastname = models.CharField(
        max_length=100
    )
    movil = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    type_client = models.CharField(
        max_length=10,
        choices=TYPES,
        default='natural'
    )

    def __str__(self):
        return f"{self.lastname} {self.name}"

    def save(self):
        self.name = self.name.upper()
        self.lastname = self.lastname.upper()
        super(Client, self).save()

    def change_status_url(self):
        return reverse("facturation:ajax_change_status", kwargs={"pk": self.pk})

    class Meta:
        verbose_name_plural = "Clients"


class InvoiceHeader(ClassModel2):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    sub_total = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    total = models.FloatField(default=0)

    def __str__(self):
        return '{}'.format(self.id)

    def save(self):
        self.total = self.sub_total - self.discount
        super(InvoiceHeader, self).save()

    class Meta:
        verbose_name_plural = 'Header Invoices'
        verbose_name = 'Header Invoice'

class InvoiceDetail(ClassModel2):
    invoice = models.ForeignKey(InvoiceHeader, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.BigIntegerField(default=0)
    price =  models.FloatField(default=0)
    sub_total = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    total = models.FloatField(default=0)

    def __str__(self):
        return '{}'.format(self.product)

    def save(self):
        self.sub_total = float(float(int(self.quantity)) * float(self.price))
        self.total = self.sub_total - float(self.discount)
        super(InvoiceDetail, self).save()

    class Meta:
        verbose_name_plural = 'Detail Invoices'
        verbose_name = 'Detail Invoice'