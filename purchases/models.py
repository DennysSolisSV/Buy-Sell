from django.db import models
from django.urls import reverse
from inventory.models import ClassModel, Product


class Vendor(ClassModel):
    description=models.CharField(
        max_length=100,
        unique=True
        )
    address=models.CharField(
        max_length=250,
        null=True, blank=True
        )
    contact=models.CharField(
        max_length=100
    )
    phone=models.CharField(
        max_length=15,
        null=True, blank=True
    )
    email=models.CharField(
        max_length=250,
        null=True, blank=True
    )

    def __str__(self):
        return '{}'.format(self.description)

    def save(self):
        self.description = self.description.upper()
        super(Vendor, self).save()

    class Meta:
        verbose_name_plural = "Vendors"


class Purchase(ClassModel):
    date_purchase = models.DateField(null=True, blank=True)
    observations = models.TextField(blank=True, null=True)
    invoice_number = models.CharField(max_length=100)
    date_invoice = models.DateField()
    sub_total = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    total = models.FloatField(default=0)

    vendor = models.ForeignKey(Vendor, on_delete = models.CASCADE)

    def __str__(self):
        return'{}'.format(self.observations)

    def save(self):
        self.observations = self.observations.upper()
        self.total = self.sub_total - self.discount
        super(Purchase, self).save()

    class Meta:
        verbose_name_plural = "Header Purchases"
        verbose_name = "Header Purchase"

    def get_absolute_url(self):
        return reverse("purchases:purchase_edit", kwargs={"pk": self.pk})

    def del_absolute_url(self):
        return reverse("purchases:purchase_del", kwargs={"pk": self.pk})

class PurchaseDetail(ClassModel):
    purchase =  models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.BigIntegerField(default=0)
    price = models.FloatField(default=0)
    sub_total = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    total = models.FloatField(default=0)
    cost =  models.FloatField(default=0)

    def __str__(self):
        return '{}'.format(self.product)

    def save(self):
        self.sub_total = float(float(self.quantity) * self.price )
        self.total = self.sub_total - self.discount
        super(PurchaseDetail,self).save()

    class Meta:
        verbose_name_plural = "Detail Purchases"
        verbose_name = "Detail Purchase"


