from django.db import models
from django.db.models import Sum
from django.urls import reverse
from inventory.models import ClassModel, Product
from django.db.models.signals import post_delete, post_save


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
        self.sub_total = float(float(self.quantity) * float(self.price) )
        self.total = float(self.sub_total) - float(self.discount)
        super(PurchaseDetail,self).save()

    class Meta:
        verbose_name_plural = "Detail Purchases"
        verbose_name = "Detail Purchase"

def post_save_purchase_detail_receiver(sender, instance, *args, **kwargs):
    # updating product existence
    product = Product.objects.get(id=instance.product.id)
    product.stock = int(product.stock) + int(instance.quantity)
    product.last_purchase = instance.purchase.date_purchase
    product.save()


post_save.connect(post_save_purchase_detail_receiver, sender=PurchaseDetail)


def post_delete_purchase_detail_receiver(sender, instance, *args, **kwargs):
    #  update the values on the purchase model 
    purchase = Purchase.objects.get(id=instance.purchase.id)
    purchase.sub_total, purchase.discount, \
    purchase.total = get_sum_totals_detail_in_purchase(purchase)
    purchase.save()

    # updating product existence
    product = Product.objects.get(id=instance.product.id)
    product.stock = product.stock - instance.quantity
    product.save()




post_delete.connect(post_delete_purchase_detail_receiver, sender=PurchaseDetail)


#  update the values on the purchase model 
def get_sum_totals_detail_in_purchase(purchase):
    detail = PurchaseDetail.objects.filter(purchase=purchase)
    if detail:
        out = detail.aggregate(Sum('sub_total'))
        out1 = detail.aggregate(Sum('discount'))
        out2 = detail.aggregate(Sum('total'))

        return (out['sub_total__sum'],
                out1['discount__sum'],
                out2['total__sum']
                )
    else:
        return 0, 0, 0