from django.db import models
from inventory.models import ClassModel

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
